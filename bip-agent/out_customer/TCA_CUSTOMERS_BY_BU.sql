/* TCA customer master extract by business unit (for MDM).
   Oracle Fusion Cloud ERP (26d), data source ApplicationDB_FSCM. Parameter :P_BU_ID (required) =
   business unit ORGANIZATION_ID.

   Grain: one row per customer account site x site contact (sites without contacts appear once).
   Bill-To and Ship-To site uses of the site are side by side. Active and end-dated records are
   ALL returned; every level carries its system IDs, ORIG_SYSTEM_REFERENCE, status, start/end
   dates, creation/last-update dates and a derived *_ACTIVE flag
   ('Y' = status active and today inside the start/end dates).

   Where a level can hold several rows (date-effective profiles, tax registrations, site uses of
   one purpose, contact points) the current row is taken, else the most recent one.

   Assumptions to confirm on your instance (marked ASSUMPTION below):
   1. Customer account sites are shared by reference data set; the BU's set is found in
      FND_SETID_ASSIGNMENTS with REFERENCE_GROUP_NAME = 'HZ_CUSTOMER_ACCOUNT_SITE'.
   2. Tax profiles: party level PARTY_TYPE_CODE = 'THIRD_PARTY', party-site level 'THIRD_PARTY_SITE'.
   3. Site contacts are HZ_CUST_ACCOUNT_ROLES rows with ROLE_TYPE = 'CONTACT' on the account site;
      their email and phone are contact points of the contact person recorded for that contact
      relationship (HZ_CONTACT_POINTS.RELATIONSHIP_ID = the role's RELATIONSHIP_ID). */
WITH bu AS (
    SELECT bu_tl.ORGANIZATION_ID AS BU_ID,
           bu_tl.NAME            AS BU_NAME,
           fsa.SET_ID            AS SITE_SET_ID
    FROM   HR_ORGANIZATION_UNITS_F_TL bu_tl
    JOIN   FND_SETID_ASSIGNMENTS fsa
           ON  fsa.DETERMINANT_VALUE    = bu_tl.ORGANIZATION_ID
           AND fsa.DETERMINANT_TYPE     = 'BU'
           AND fsa.REFERENCE_GROUP_NAME = 'HZ_CUSTOMER_ACCOUNT_SITE'          -- ASSUMPTION 1
    WHERE  bu_tl.ORGANIZATION_ID = :P_BU_ID
    AND    bu_tl.LANGUAGE        = USERENV('LANG')
    AND    TRUNC(SYSDATE) BETWEEN bu_tl.EFFECTIVE_START_DATE AND bu_tl.EFFECTIVE_END_DATE
),
-- one Bill-To and one Ship-To use per account site: the active one, else the latest
site_use AS (
    SELECT su.SITE_USE_ID, su.CUST_ACCT_SITE_ID, su.SITE_USE_CODE, su.LOCATION, su.PRIMARY_FLAG,
           su.BILL_TO_SITE_USE_ID, su.PAYMENT_TERM_ID, su.TAX_CLASSIFICATION, su.TAX_REFERENCE,
           su.SIC_CODE, su.TERRITORY_ID, su.SET_ID, su.ORIG_SYSTEM_REFERENCE, su.STATUS,
           su.START_DATE, su.END_DATE, su.CREATION_DATE, su.LAST_UPDATE_DATE,
           ROW_NUMBER() OVER (PARTITION BY su.CUST_ACCT_SITE_ID, su.SITE_USE_CODE
                              ORDER BY CASE WHEN su.STATUS = 'A' THEN 0 ELSE 1 END,
                                       su.START_DATE DESC NULLS LAST, su.SITE_USE_ID DESC) AS RN
    FROM   HZ_CUST_SITE_USES_ALL su
    WHERE  su.SITE_USE_CODE IN ('BILL_TO', 'SHIP_TO')
),
-- date-effective customer profiles: the row effective today, else the latest
cust_prof AS (
    SELECT pf.CUST_ACCOUNT_PROFILE_ID, pf.CUST_ACCOUNT_ID, pf.SITE_USE_ID, pf.PROFILE_CLASS_ID,
           pf.STANDARD_TERMS, pf.COLLECTOR_ID, pf.CREDIT_CHECKING, pf.CREDIT_HOLD, pf.CREDIT_LIMIT,
           pf.CREDIT_CURRENCY_CODE, pf.CREDIT_CLASSIFICATION, pf.CREDIT_RATING, pf.RISK_CODE,
           pf.ACCOUNT_STATUS, pf.TOLERANCE, pf.DUNNING_LETTERS, pf.SEND_STATEMENTS,
           pf.STATEMENT_CYCLE_ID, pf.TXN_DELIVERY_METHOD, pf.STMT_DELIVERY_METHOD, pf.STATUS,
           pf.EFFECTIVE_START_DATE, pf.EFFECTIVE_END_DATE,
           ROW_NUMBER() OVER (PARTITION BY pf.CUST_ACCOUNT_ID, pf.SITE_USE_ID
                              ORDER BY CASE WHEN TRUNC(SYSDATE) BETWEEN pf.EFFECTIVE_START_DATE
                                                 AND pf.EFFECTIVE_END_DATE THEN 0 ELSE 1 END,
                                       pf.EFFECTIVE_START_DATE DESC) AS RN
    FROM   HZ_CUSTOMER_PROFILES_F pf
),
-- default tax registration per tax profile: effective today, else the latest
tax_reg AS (
    SELECT r.REGISTRATION_ID, r.PARTY_TAX_PROFILE_ID, r.REGISTRATION_NUMBER, r.REGISTRATION_TYPE_CODE,
           r.TAX_REGIME_CODE, r.TAX, r.TAX_JURISDICTION_CODE, r.REGISTRATION_STATUS_CODE,
           r.REGISTRATION_SOURCE_CODE, r.REGISTRATION_REASON_CODE, r.EFFECTIVE_FROM, r.EFFECTIVE_TO,
           ROW_NUMBER() OVER (PARTITION BY r.PARTY_TAX_PROFILE_ID
                              ORDER BY CASE WHEN TRUNC(SYSDATE) BETWEEN TRUNC(r.EFFECTIVE_FROM)
                                                 AND NVL(TRUNC(r.EFFECTIVE_TO), TRUNC(SYSDATE))
                                            THEN 0 ELSE 1 END,
                                       r.EFFECTIVE_FROM DESC) AS RN
    FROM   ZX_REGISTRATIONS r
    WHERE  r.DEFAULT_REGISTRATION_FLAG = 'Y'
),
-- contact points of a contact person within a relationship: active primary first, else latest
contact_pt AS (
    SELECT cp.CONTACT_POINT_ID, cp.OWNER_TABLE_ID, cp.RELATIONSHIP_ID, cp.CONTACT_POINT_TYPE,
           cp.EMAIL_ADDRESS, cp.PHONE_COUNTRY_CODE, cp.PHONE_AREA_CODE, cp.PHONE_NUMBER,
           cp.PHONE_EXTENSION, cp.PHONE_LINE_TYPE, cp.PRIMARY_FLAG, cp.STATUS, cp.START_DATE, cp.END_DATE,
           ROW_NUMBER() OVER (PARTITION BY cp.OWNER_TABLE_ID, cp.RELATIONSHIP_ID, cp.CONTACT_POINT_TYPE
                              ORDER BY CASE WHEN cp.STATUS = 'A' THEN 0 ELSE 1 END,
                                       CASE WHEN cp.PRIMARY_FLAG = 'Y' THEN 0 ELSE 1 END,
                                       cp.START_DATE DESC NULLS LAST, cp.CONTACT_POINT_ID DESC) AS RN
    FROM   HZ_CONTACT_POINTS cp
    WHERE  cp.OWNER_TABLE_NAME = 'HZ_PARTIES'
    AND    cp.CONTACT_POINT_TYPE IN ('EMAIL', 'PHONE')
)
SELECT
       -- ===== Business unit
       bu.BU_ID                         AS BU_ID,
       bu.BU_NAME                       AS BU_NAME,
       bu.SITE_SET_ID                   AS REFERENCE_SET_ID,
       -- ===== Party (HZ_PARTIES)
       hp.PARTY_ID                      AS PARTY_ID,
       hp.PARTY_NUMBER                  AS PARTY_NUMBER,
       hp.PARTY_NAME                    AS PARTY_NAME,
       hp.PARTY_TYPE                    AS PARTY_TYPE,
       hp.ORIG_SYSTEM_REFERENCE         AS PARTY_ORIG_SYSTEM_REF,
       hp.JGZZ_FISCAL_CODE              AS PARTY_TAXPAYER_ID,
       hp.DUNS_NUMBER_C                 AS PARTY_DUNS_NUMBER,
       hp.SIC_CODE_TYPE                 AS PARTY_SIC_CODE_TYPE,
       hp.SIC_CODE                      AS PARTY_SIC_CODE,
       hp.CATEGORY_CODE                 AS PARTY_CATEGORY,
       hp.URL                           AS PARTY_URL,
       hp.EMAIL_ADDRESS                 AS PARTY_EMAIL,
       hp.PRIMARY_PHONE_COUNTRY_CODE    AS PARTY_PHONE_COUNTRY_CODE,
       hp.PRIMARY_PHONE_AREA_CODE       AS PARTY_PHONE_AREA_CODE,
       hp.PRIMARY_PHONE_NUMBER          AS PARTY_PHONE_NUMBER,
       hp.STATUS                        AS PARTY_STATUS,
       CASE WHEN hp.STATUS = 'A' THEN 'Y' ELSE 'N' END AS PARTY_ACTIVE,
       hp.CREATION_DATE                 AS PARTY_CREATION_DATE,
       hp.LAST_UPDATE_DATE              AS PARTY_LAST_UPDATE_DATE,
       -- ===== Party-level tax profile (ZX)
       pty_tax.PARTY_TAX_PROFILE_ID     AS PARTY_TAX_PROFILE_ID,
       pty_tax.REP_REGISTRATION_NUMBER  AS PARTY_TAX_REGISTRATION_NUMBER,
       pty_tax.REGISTRATION_TYPE_CODE   AS PARTY_TAX_REGISTRATION_TYPE,
       pty_tax.COUNTRY_CODE             AS PARTY_TAX_COUNTRY,
       pty_tax.TAX_CLASSIFICATION_CODE  AS PARTY_TAX_CLASSIFICATION,
       pty_tax.ROUNDING_LEVEL_CODE      AS PARTY_TAX_ROUNDING_LEVEL,
       pty_tax.ROUNDING_RULE_CODE       AS PARTY_TAX_ROUNDING_RULE,
       pty_tax.INCLUSIVE_TAX_FLAG       AS PARTY_TAX_INCLUSIVE_FLAG,
       pty_reg.REGISTRATION_ID          AS PARTY_TAX_REG_ID,
       pty_reg.REGISTRATION_NUMBER      AS PARTY_TAX_REG_NUMBER,
       pty_reg.TAX_REGIME_CODE          AS PARTY_TAX_REG_REGIME,
       pty_reg.REGISTRATION_STATUS_CODE AS PARTY_TAX_REG_STATUS,
       pty_reg.EFFECTIVE_FROM           AS PARTY_TAX_REG_START_DATE,
       pty_reg.EFFECTIVE_TO             AS PARTY_TAX_REG_END_DATE,
       -- ===== Customer account (HZ_CUST_ACCOUNTS)
       hca.CUST_ACCOUNT_ID              AS CUST_ACCOUNT_ID,
       hca.ACCOUNT_NUMBER               AS ACCOUNT_NUMBER,
       hca.ACCOUNT_NAME                 AS ACCOUNT_NAME,
       hca.ORIG_SYSTEM_REFERENCE        AS ACCOUNT_ORIG_SYSTEM_REF,
       hca.CUSTOMER_TYPE                AS ACCOUNT_CUSTOMER_TYPE,
       hca.CUSTOMER_CLASS_CODE          AS ACCOUNT_CUSTOMER_CLASS,
       hca.SOURCE_CODE                  AS ACCOUNT_SOURCE_CODE,
       hca.TAX_CODE                     AS ACCOUNT_TAX_CODE,
       hca.HOLD_BILL_FLAG               AS ACCOUNT_HOLD_BILL_FLAG,
       hca.AUTOPAY_FLAG                 AS ACCOUNT_AUTOPAY_FLAG,
       hca.SELLING_PARTY_ID             AS ACCOUNT_SELLING_PARTY_ID,
       hca.STATUS                       AS ACCOUNT_STATUS,
       hca.ACCOUNT_ESTABLISHED_DATE     AS ACCOUNT_START_DATE,
       hca.ACCOUNT_TERMINATION_DATE     AS ACCOUNT_END_DATE,
       hca.STATUS_UPDATE_DATE           AS ACCOUNT_STATUS_UPDATE_DATE,
       CASE WHEN hca.STATUS = 'A'
             AND TRUNC(SYSDATE) BETWEEN NVL(TRUNC(hca.ACCOUNT_ESTABLISHED_DATE), TRUNC(SYSDATE))
                                    AND NVL(TRUNC(hca.ACCOUNT_TERMINATION_DATE), TRUNC(SYSDATE))
            THEN 'Y' ELSE 'N' END       AS ACCOUNT_ACTIVE,
       hca.CREATION_DATE                AS ACCOUNT_CREATION_DATE,
       hca.LAST_UPDATE_DATE             AS ACCOUNT_LAST_UPDATE_DATE,
       -- ===== Account-level profile (HZ_CUSTOMER_PROFILES_F row without site use)
       acct_prof.CUST_ACCOUNT_PROFILE_ID AS ACCOUNT_PROFILE_ID,
       acct_prof.PROFILE_CLASS_ID       AS ACCOUNT_PROFILE_CLASS_ID,
       acct_pc.NAME                     AS ACCOUNT_PROFILE_CLASS,
       acct_prof.STANDARD_TERMS         AS ACCOUNT_PAYMENT_TERM_ID,
       acct_term.NAME                   AS ACCOUNT_PAYMENT_TERM,
       acct_prof.COLLECTOR_ID           AS ACCOUNT_COLLECTOR_ID,
       acct_coll.NAME                   AS ACCOUNT_COLLECTOR,
       acct_prof.CREDIT_CHECKING        AS ACCOUNT_CREDIT_CHECK,
       acct_prof.CREDIT_HOLD            AS ACCOUNT_CREDIT_HOLD,
       acct_prof.CREDIT_LIMIT           AS ACCOUNT_CREDIT_LIMIT,
       acct_prof.CREDIT_CURRENCY_CODE   AS ACCOUNT_CREDIT_CURRENCY,
       acct_prof.CREDIT_CLASSIFICATION  AS ACCOUNT_CREDIT_CLASSIFICATION,
       acct_prof.CREDIT_RATING          AS ACCOUNT_CREDIT_RATING,
       acct_prof.RISK_CODE              AS ACCOUNT_RISK_CODE,
       acct_prof.ACCOUNT_STATUS         AS ACCOUNT_PROFILE_ACCT_STATUS,
       acct_prof.TOLERANCE              AS ACCOUNT_CREDIT_TOLERANCE,
       acct_prof.DUNNING_LETTERS        AS ACCOUNT_DUNNING_LETTERS,
       acct_prof.SEND_STATEMENTS        AS ACCOUNT_SEND_STATEMENTS,
       acct_prof.STATEMENT_CYCLE_ID     AS ACCOUNT_STATEMENT_CYCLE_ID,
       acct_prof.TXN_DELIVERY_METHOD    AS ACCOUNT_TXN_DELIVERY_METHOD,
       acct_prof.STMT_DELIVERY_METHOD   AS ACCOUNT_STMT_DELIVERY_METHOD,
       acct_prof.STATUS                 AS ACCOUNT_PROFILE_STATUS,
       acct_prof.EFFECTIVE_START_DATE   AS ACCOUNT_PROFILE_START_DATE,
       acct_prof.EFFECTIVE_END_DATE     AS ACCOUNT_PROFILE_END_DATE,
       CASE WHEN acct_prof.STATUS = 'A'
             AND TRUNC(SYSDATE) BETWEEN acct_prof.EFFECTIVE_START_DATE AND acct_prof.EFFECTIVE_END_DATE
            THEN 'Y' ELSE 'N' END       AS ACCOUNT_PROFILE_ACTIVE,
       -- ===== Party site (HZ_PARTY_SITES)
       hps.PARTY_SITE_ID                AS PARTY_SITE_ID,
       hps.PARTY_SITE_NUMBER            AS PARTY_SITE_NUMBER,
       hps.PARTY_SITE_NAME              AS PARTY_SITE_NAME,
       hps.ORIG_SYSTEM_REFERENCE        AS PARTY_SITE_ORIG_SYSTEM_REF,
       hps.IDENTIFYING_ADDRESS_FLAG     AS PARTY_SITE_IDENTIFYING_FLAG,
       hps.ADDRESSEE                    AS PARTY_SITE_ADDRESSEE,
       hps.GLOBAL_LOCATION_NUMBER       AS PARTY_SITE_GLN,
       hps.STATUS                       AS PARTY_SITE_STATUS,
       hps.START_DATE_ACTIVE            AS PARTY_SITE_START_DATE,
       hps.END_DATE_ACTIVE              AS PARTY_SITE_END_DATE,
       CASE WHEN hps.STATUS = 'A'
             AND TRUNC(SYSDATE) BETWEEN NVL(TRUNC(hps.START_DATE_ACTIVE), TRUNC(SYSDATE))
                                    AND NVL(TRUNC(hps.END_DATE_ACTIVE), TRUNC(SYSDATE))
            THEN 'Y' ELSE 'N' END       AS PARTY_SITE_ACTIVE,
       hps.CREATION_DATE                AS PARTY_SITE_CREATION_DATE,
       hps.LAST_UPDATE_DATE             AS PARTY_SITE_LAST_UPDATE_DATE,
       -- ===== Location (HZ_LOCATIONS)
       hl.LOCATION_ID                   AS LOCATION_ID,
       hl.ORIG_SYSTEM_REFERENCE         AS LOCATION_ORIG_SYSTEM_REF,
       hl.ADDRESS1                      AS ADDRESS_LINE1,
       hl.ADDRESS2                      AS ADDRESS_LINE2,
       hl.ADDRESS3                      AS ADDRESS_LINE3,
       hl.ADDRESS4                      AS ADDRESS_LINE4,
       hl.BUILDING                      AS BUILDING,
       hl.FLOOR_NUMBER                  AS FLOOR_NUMBER,
       hl.CITY                          AS CITY,
       hl.COUNTY                        AS COUNTY,
       hl.STATE                         AS STATE,
       hl.PROVINCE                      AS PROVINCE,
       hl.POSTAL_CODE                   AS POSTAL_CODE,
       hl.POSTAL_PLUS4_CODE             AS POSTAL_PLUS4_CODE,
       hl.COUNTRY                       AS COUNTRY,
       hl.ADDRESS_STYLE                 AS ADDRESS_STYLE,
       hl.TIMEZONE_CODE                 AS TIMEZONE_CODE,
       hl.LATITUDE                      AS LATITUDE,
       hl.LONGITUDE                     AS LONGITUDE,
       hl.VALIDATED_FLAG                AS ADDRESS_VALIDATED_FLAG,
       hl.VALIDATION_STATUS_CODE        AS ADDRESS_VALIDATION_STATUS,
       hl.STATUS_FLAG                   AS LOCATION_STATUS,
       hl.ADDRESS_EFFECTIVE_DATE        AS LOCATION_START_DATE,
       hl.ADDRESS_EXPIRATION_DATE       AS LOCATION_END_DATE,
       CASE WHEN TRUNC(SYSDATE) BETWEEN NVL(TRUNC(hl.ADDRESS_EFFECTIVE_DATE), TRUNC(SYSDATE))
                                    AND NVL(TRUNC(hl.ADDRESS_EXPIRATION_DATE), TRUNC(SYSDATE))
            THEN 'Y' ELSE 'N' END       AS LOCATION_ACTIVE,
       hl.CREATION_DATE                 AS LOCATION_CREATION_DATE,
       hl.LAST_UPDATE_DATE              AS LOCATION_LAST_UPDATE_DATE,
       -- ===== Account site (HZ_CUST_ACCT_SITES_ALL)
       hcas.CUST_ACCT_SITE_ID           AS CUST_ACCT_SITE_ID,
       hcas.SET_ID                      AS ACCT_SITE_SET_ID,
       hcas.ORIG_SYSTEM_REFERENCE       AS ACCT_SITE_ORIG_SYSTEM_REF,
       hcas.BILL_TO_FLAG                AS ACCT_SITE_BILL_TO_FLAG,
       hcas.SHIP_TO_FLAG                AS ACCT_SITE_SHIP_TO_FLAG,
       hcas.MARKET_FLAG                 AS ACCT_SITE_MARKET_FLAG,
       hcas.CUSTOMER_CATEGORY_CODE      AS ACCT_SITE_CUSTOMER_CATEGORY,
       hcas.KEY_ACCOUNT_FLAG            AS ACCT_SITE_KEY_ACCOUNT_FLAG,
       hcas.TRANSLATED_CUSTOMER_NAME    AS ACCT_SITE_TRANSLATED_NAME,
       hcas.ACCT_SITE_LANGUAGE          AS ACCT_SITE_LANGUAGE,
       hcas.STATUS                      AS ACCT_SITE_STATUS,
       hcas.START_DATE                  AS ACCT_SITE_START_DATE,
       hcas.END_DATE                    AS ACCT_SITE_END_DATE,
       CASE WHEN hcas.STATUS = 'A'
             AND TRUNC(SYSDATE) BETWEEN NVL(TRUNC(hcas.START_DATE), TRUNC(SYSDATE))
                                    AND NVL(TRUNC(hcas.END_DATE), TRUNC(SYSDATE))
            THEN 'Y' ELSE 'N' END       AS ACCT_SITE_ACTIVE,
       hcas.CREATION_DATE               AS ACCT_SITE_CREATION_DATE,
       hcas.LAST_UPDATE_DATE            AS ACCT_SITE_LAST_UPDATE_DATE,
       -- ===== Bill-To site use (HZ_CUST_SITE_USES_ALL)
       bill.SITE_USE_ID                 AS BILL_TO_SITE_USE_ID,
       bill.LOCATION                    AS BILL_TO_LOCATION,
       bill.PRIMARY_FLAG                AS BILL_TO_PRIMARY_FLAG,
       bill.ORIG_SYSTEM_REFERENCE       AS BILL_TO_ORIG_SYSTEM_REF,
       bill.PAYMENT_TERM_ID             AS BILL_TO_PAYMENT_TERM_ID,
       bill_term.NAME                   AS BILL_TO_PAYMENT_TERM,
       bill.TAX_CLASSIFICATION          AS BILL_TO_TAX_CLASSIFICATION,
       bill.TAX_REFERENCE               AS BILL_TO_TAXPAYER_ID,
       bill.SIC_CODE                    AS BILL_TO_SIC_CODE,
       bill.TERRITORY_ID                AS BILL_TO_TERRITORY_ID,
       bill.SET_ID                      AS BILL_TO_SET_ID,
       bill.STATUS                      AS BILL_TO_STATUS,
       bill.START_DATE                  AS BILL_TO_START_DATE,
       bill.END_DATE                    AS BILL_TO_END_DATE,
       CASE WHEN bill.STATUS = 'A'
             AND TRUNC(SYSDATE) BETWEEN NVL(TRUNC(bill.START_DATE), TRUNC(SYSDATE))
                                    AND NVL(TRUNC(bill.END_DATE), TRUNC(SYSDATE))
            THEN 'Y' ELSE 'N' END       AS BILL_TO_ACTIVE,
       bill.CREATION_DATE               AS BILL_TO_CREATION_DATE,
       bill.LAST_UPDATE_DATE            AS BILL_TO_LAST_UPDATE_DATE,
       -- ===== Site-level profile (HZ_CUSTOMER_PROFILES_F row for the Bill-To use)
       site_prof.CUST_ACCOUNT_PROFILE_ID AS SITE_PROFILE_ID,
       site_prof.PROFILE_CLASS_ID       AS SITE_PROFILE_CLASS_ID,
       site_pc.NAME                     AS SITE_PROFILE_CLASS,
       site_prof.STANDARD_TERMS         AS SITE_PAYMENT_TERM_ID,
       site_term.NAME                   AS SITE_PAYMENT_TERM,
       site_prof.COLLECTOR_ID           AS SITE_COLLECTOR_ID,
       site_coll.NAME                   AS SITE_COLLECTOR,
       site_prof.CREDIT_CHECKING        AS SITE_CREDIT_CHECK,
       site_prof.CREDIT_HOLD            AS SITE_CREDIT_HOLD,
       site_prof.CREDIT_LIMIT           AS SITE_CREDIT_LIMIT,
       site_prof.CREDIT_CURRENCY_CODE   AS SITE_CREDIT_CURRENCY,
       site_prof.DUNNING_LETTERS        AS SITE_DUNNING_LETTERS,
       site_prof.SEND_STATEMENTS        AS SITE_SEND_STATEMENTS,
       site_prof.TXN_DELIVERY_METHOD    AS SITE_TXN_DELIVERY_METHOD,
       site_prof.STMT_DELIVERY_METHOD   AS SITE_STMT_DELIVERY_METHOD,
       site_prof.STATUS                 AS SITE_PROFILE_STATUS,
       site_prof.EFFECTIVE_START_DATE   AS SITE_PROFILE_START_DATE,
       site_prof.EFFECTIVE_END_DATE     AS SITE_PROFILE_END_DATE,
       CASE WHEN site_prof.STATUS = 'A'
             AND TRUNC(SYSDATE) BETWEEN site_prof.EFFECTIVE_START_DATE AND site_prof.EFFECTIVE_END_DATE
            THEN 'Y' ELSE 'N' END       AS SITE_PROFILE_ACTIVE,
       -- ===== Ship-To site use (HZ_CUST_SITE_USES_ALL)
       ship.SITE_USE_ID                 AS SHIP_TO_SITE_USE_ID,
       ship.BILL_TO_SITE_USE_ID         AS SHIP_TO_LINKED_BILL_TO_ID,
       ship.LOCATION                    AS SHIP_TO_LOCATION,
       ship.PRIMARY_FLAG                AS SHIP_TO_PRIMARY_FLAG,
       ship.ORIG_SYSTEM_REFERENCE       AS SHIP_TO_ORIG_SYSTEM_REF,
       ship.TAX_CLASSIFICATION          AS SHIP_TO_TAX_CLASSIFICATION,
       ship.TERRITORY_ID                AS SHIP_TO_TERRITORY_ID,
       ship.SET_ID                      AS SHIP_TO_SET_ID,
       ship.STATUS                      AS SHIP_TO_STATUS,
       ship.START_DATE                  AS SHIP_TO_START_DATE,
       ship.END_DATE                    AS SHIP_TO_END_DATE,
       CASE WHEN ship.STATUS = 'A'
             AND TRUNC(SYSDATE) BETWEEN NVL(TRUNC(ship.START_DATE), TRUNC(SYSDATE))
                                    AND NVL(TRUNC(ship.END_DATE), TRUNC(SYSDATE))
            THEN 'Y' ELSE 'N' END       AS SHIP_TO_ACTIVE,
       ship.CREATION_DATE               AS SHIP_TO_CREATION_DATE,
       ship.LAST_UPDATE_DATE            AS SHIP_TO_LAST_UPDATE_DATE,
       -- ===== Site-level tax profile (ZX_PARTY_TAX_PROFILE for the party site)
       site_tax.PARTY_TAX_PROFILE_ID    AS SITE_TAX_PROFILE_ID,
       site_tax.REP_REGISTRATION_NUMBER AS SITE_TAX_REGISTRATION_NUMBER,
       site_tax.REGISTRATION_TYPE_CODE  AS SITE_TAX_REGISTRATION_TYPE,
       site_tax.COUNTRY_CODE            AS SITE_TAX_COUNTRY,
       site_tax.TAX_CLASSIFICATION_CODE AS SITE_TAX_CLASSIFICATION,
       site_tax.ROUNDING_LEVEL_CODE     AS SITE_TAX_ROUNDING_LEVEL,
       site_tax.ROUNDING_RULE_CODE      AS SITE_TAX_ROUNDING_RULE,
       site_tax.INCLUSIVE_TAX_FLAG      AS SITE_TAX_INCLUSIVE_FLAG,
       site_tax.PROCESS_FOR_APPLICABILITY_FLAG AS SITE_TAX_APPLICABILITY_FLAG,
       site_tax.ALLOW_OFFSET_TAX_FLAG   AS SITE_TAX_ALLOW_OFFSET_FLAG,
       site_tax.SELF_ASSESS_FLAG        AS SITE_TAX_SELF_ASSESS_FLAG,
       site_tax.TAX_REG_VALIDATION_STATUS_CODE AS SITE_TAX_REG_VALIDATION_STATUS,
       -- ===== Site tax profile's default registration (ZX_REGISTRATIONS)
       site_reg.REGISTRATION_ID         AS SITE_TAX_REG_ID,
       site_reg.REGISTRATION_NUMBER     AS SITE_TAX_REG_NUMBER,
       site_reg.REGISTRATION_TYPE_CODE  AS SITE_TAX_REG_TYPE,
       site_reg.TAX_REGIME_CODE         AS SITE_TAX_REG_REGIME,
       site_reg.TAX                     AS SITE_TAX_REG_TAX,
       site_reg.TAX_JURISDICTION_CODE   AS SITE_TAX_REG_JURISDICTION,
       site_reg.REGISTRATION_SOURCE_CODE AS SITE_TAX_REG_SOURCE,
       site_reg.REGISTRATION_REASON_CODE AS SITE_TAX_REG_REASON,
       site_reg.REGISTRATION_STATUS_CODE AS SITE_TAX_REG_STATUS,
       site_reg.EFFECTIVE_FROM          AS SITE_TAX_REG_START_DATE,
       site_reg.EFFECTIVE_TO            AS SITE_TAX_REG_END_DATE,
       CASE WHEN site_reg.REGISTRATION_ID IS NOT NULL
             AND TRUNC(SYSDATE) BETWEEN TRUNC(site_reg.EFFECTIVE_FROM)
                                    AND NVL(TRUNC(site_reg.EFFECTIVE_TO), TRUNC(SYSDATE))
            THEN 'Y' ELSE 'N' END       AS SITE_TAX_REG_ACTIVE,
       -- ===== Site contact (HZ_CUST_ACCOUNT_ROLES, HZ_RELATIONSHIPS, HZ_ORG_CONTACTS, HZ_PARTIES)
       car.CUST_ACCOUNT_ROLE_ID         AS CONTACT_ROLE_ID,
       car.RELATIONSHIP_ID              AS CONTACT_RELATIONSHIP_ID,
       rel.RELATIONSHIP_REC_ID          AS CONTACT_RELATIONSHIP_REC_ID,
       cont.PARTY_ID                    AS CONTACT_PERSON_PARTY_ID,
       hoc.ORG_CONTACT_ID               AS ORG_CONTACT_ID,
       car.ORIG_SYSTEM_REFERENCE        AS CONTACT_ORIG_SYSTEM_REF,
       cont.PARTY_NUMBER                AS CONTACT_PARTY_NUMBER,
       cont.PERSON_TITLE                AS CONTACT_TITLE,
       cont.PERSON_FIRST_NAME           AS CONTACT_FIRST_NAME,
       cont.PERSON_MIDDLE_NAME          AS CONTACT_MIDDLE_NAME,
       cont.PERSON_LAST_NAME            AS CONTACT_LAST_NAME,
       hoc.CONTACT_NUMBER               AS CONTACT_NUMBER,
       hoc.JOB_TITLE                    AS CONTACT_JOB_TITLE,
       hoc.DEPARTMENT                   AS CONTACT_DEPARTMENT,
       car.PRIMARY_FLAG                 AS CONTACT_PRIMARY_FLAG,
       cont.STATUS                      AS CONTACT_PERSON_STATUS,
       car.STATUS                       AS CONTACT_ROLE_STATUS,
       rel.STATUS                       AS CONTACT_RELATIONSHIP_STATUS,
       rel.START_DATE                   AS CONTACT_START_DATE,
       rel.END_DATE                     AS CONTACT_END_DATE,
       CASE WHEN car.STATUS = 'A' AND rel.STATUS = 'A'
             AND TRUNC(SYSDATE) BETWEEN NVL(TRUNC(rel.START_DATE), TRUNC(SYSDATE))
                                    AND NVL(TRUNC(rel.END_DATE), TRUNC(SYSDATE))
            THEN 'Y' ELSE 'N' END       AS CONTACT_ACTIVE,
       em.CONTACT_POINT_ID              AS CONTACT_EMAIL_POINT_ID,
       em.EMAIL_ADDRESS                 AS CONTACT_EMAIL,
       em.STATUS                        AS CONTACT_EMAIL_STATUS,
       em.START_DATE                    AS CONTACT_EMAIL_START_DATE,
       em.END_DATE                      AS CONTACT_EMAIL_END_DATE,
       ph.CONTACT_POINT_ID              AS CONTACT_PHONE_POINT_ID,
       ph.PHONE_COUNTRY_CODE            AS CONTACT_PHONE_COUNTRY_CODE,
       ph.PHONE_AREA_CODE               AS CONTACT_PHONE_AREA_CODE,
       ph.PHONE_NUMBER                  AS CONTACT_PHONE_NUMBER,
       ph.PHONE_EXTENSION               AS CONTACT_PHONE_EXTENSION,
       ph.PHONE_LINE_TYPE               AS CONTACT_PHONE_LINE_TYPE,
       ph.STATUS                        AS CONTACT_PHONE_STATUS,
       ph.START_DATE                    AS CONTACT_PHONE_START_DATE,
       ph.END_DATE                      AS CONTACT_PHONE_END_DATE
FROM   bu
JOIN   HZ_CUST_ACCT_SITES_ALL hcas
       ON  hcas.SET_ID = bu.SITE_SET_ID
JOIN   HZ_CUST_ACCOUNTS hca
       ON  hca.CUST_ACCOUNT_ID = hcas.CUST_ACCOUNT_ID
JOIN   HZ_PARTIES hp
       ON  hp.PARTY_ID = hca.PARTY_ID
JOIN   HZ_PARTY_SITES hps
       ON  hps.PARTY_SITE_ID = hcas.PARTY_SITE_ID
JOIN   HZ_LOCATIONS hl
       ON  hl.LOCATION_ID = hps.LOCATION_ID
-- party-level tax profile and its default registration
LEFT JOIN ZX_PARTY_TAX_PROFILE pty_tax
       ON  pty_tax.PARTY_ID = hp.PARTY_ID
       AND pty_tax.PARTY_TYPE_CODE = 'THIRD_PARTY'                            -- ASSUMPTION 2
LEFT JOIN tax_reg pty_reg
       ON  pty_reg.PARTY_TAX_PROFILE_ID = pty_tax.PARTY_TAX_PROFILE_ID
       AND pty_reg.RN = 1
-- account-level profile
LEFT JOIN cust_prof acct_prof
       ON  acct_prof.CUST_ACCOUNT_ID = hca.CUST_ACCOUNT_ID
       AND acct_prof.SITE_USE_ID IS NULL
       AND acct_prof.RN = 1
LEFT JOIN HZ_CUST_PROFILE_CLASSES acct_pc
       ON  acct_pc.PROFILE_CLASS_ID = acct_prof.PROFILE_CLASS_ID
LEFT JOIN RA_TERMS_TL acct_term
       ON  acct_term.TERM_ID = acct_prof.STANDARD_TERMS
       AND acct_term.LANGUAGE = USERENV('LANG')
LEFT JOIN AR_COLLECTORS acct_coll
       ON  acct_coll.COLLECTOR_ID = acct_prof.COLLECTOR_ID
-- Bill-To and Ship-To uses of the account site
LEFT JOIN site_use bill
       ON  bill.CUST_ACCT_SITE_ID = hcas.CUST_ACCT_SITE_ID
       AND bill.SITE_USE_CODE = 'BILL_TO'
       AND bill.RN = 1
LEFT JOIN RA_TERMS_TL bill_term
       ON  bill_term.TERM_ID = bill.PAYMENT_TERM_ID
       AND bill_term.LANGUAGE = USERENV('LANG')
LEFT JOIN site_use ship
       ON  ship.CUST_ACCT_SITE_ID = hcas.CUST_ACCT_SITE_ID
       AND ship.SITE_USE_CODE = 'SHIP_TO'
       AND ship.RN = 1
-- site-level profile (on the Bill-To use)
LEFT JOIN cust_prof site_prof
       ON  site_prof.SITE_USE_ID = bill.SITE_USE_ID
       AND site_prof.RN = 1
LEFT JOIN HZ_CUST_PROFILE_CLASSES site_pc
       ON  site_pc.PROFILE_CLASS_ID = site_prof.PROFILE_CLASS_ID
LEFT JOIN RA_TERMS_TL site_term
       ON  site_term.TERM_ID = site_prof.STANDARD_TERMS
       AND site_term.LANGUAGE = USERENV('LANG')
LEFT JOIN AR_COLLECTORS site_coll
       ON  site_coll.COLLECTOR_ID = site_prof.COLLECTOR_ID
-- site-level tax profile and its default registration
LEFT JOIN ZX_PARTY_TAX_PROFILE site_tax
       ON  site_tax.PARTY_ID = hps.PARTY_SITE_ID
       AND site_tax.PARTY_TYPE_CODE = 'THIRD_PARTY_SITE'                      -- ASSUMPTION 2
LEFT JOIN tax_reg site_reg
       ON  site_reg.PARTY_TAX_PROFILE_ID = site_tax.PARTY_TAX_PROFILE_ID
       AND site_reg.RN = 1
-- site contacts with their relationship, contact person, email and phone
LEFT JOIN HZ_CUST_ACCOUNT_ROLES car
       ON  car.CUST_ACCT_SITE_ID = hcas.CUST_ACCT_SITE_ID
       AND car.ROLE_TYPE = 'CONTACT'                                          -- ASSUMPTION 3
LEFT JOIN HZ_RELATIONSHIPS rel
       ON  rel.RELATIONSHIP_ID = car.RELATIONSHIP_ID
       AND rel.SUBJECT_ID = car.CONTACT_PERSON_ID
LEFT JOIN HZ_PARTIES cont
       ON  cont.PARTY_ID = car.CONTACT_PERSON_ID
LEFT JOIN HZ_ORG_CONTACTS hoc
       ON  hoc.PARTY_RELATIONSHIP_ID = car.RELATIONSHIP_ID
LEFT JOIN contact_pt em
       ON  em.OWNER_TABLE_ID = car.CONTACT_PERSON_ID
       AND em.RELATIONSHIP_ID = car.RELATIONSHIP_ID                           -- ASSUMPTION 3
       AND em.CONTACT_POINT_TYPE = 'EMAIL'
       AND em.RN = 1
LEFT JOIN contact_pt ph
       ON  ph.OWNER_TABLE_ID = car.CONTACT_PERSON_ID
       AND ph.RELATIONSHIP_ID = car.RELATIONSHIP_ID                           -- ASSUMPTION 3
       AND ph.CONTACT_POINT_TYPE = 'PHONE'
       AND ph.RN = 1
ORDER BY hp.PARTY_NAME, hca.ACCOUNT_NUMBER, hps.PARTY_SITE_NUMBER,
         cont.PERSON_LAST_NAME, cont.PERSON_FIRST_NAME
