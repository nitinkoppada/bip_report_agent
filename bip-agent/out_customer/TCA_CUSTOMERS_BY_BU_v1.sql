/* TCA customers by business unit: one row per active Bill-To / Ship-To site use.
   Oracle Fusion Cloud ERP (26d), data source ApplicationDB_FSCM.
   Parameter :P_BU_ID (required) = business unit ORGANIZATION_ID.

   Assumptions to confirm on your instance (marked ASSUMPTION below):
   1. Customer account sites are shared by reference data set; the BU's set is found in
      FND_SETID_ASSIGNMENTS with REFERENCE_GROUP_NAME = 'HZ_CUSTOMER_ACCOUNT_SITE'.
   2. Site-level tax profiles have ZX_PARTY_TAX_PROFILE.PARTY_TYPE_CODE = 'THIRD_PARTY_SITE'.
   3. One default, currently effective tax registration per site tax profile; if a site has
      default registrations in several tax regimes, it returns one row per regime. */
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
)
SELECT
       -- Business unit
       bu.BU_NAME                      AS BUSINESS_UNIT,
       -- Party and account
       hp.PARTY_NUMBER                 AS PARTY_NUMBER,
       hp.PARTY_NAME                   AS CUSTOMER_NAME,
       hp.PARTY_TYPE                   AS PARTY_TYPE,
       hca.ACCOUNT_NUMBER              AS ACCOUNT_NUMBER,
       hca.ACCOUNT_NAME                AS ACCOUNT_DESCRIPTION,
       hca.CUSTOMER_TYPE               AS CUSTOMER_TYPE,
       hca.CUSTOMER_CLASS_CODE         AS CUSTOMER_CLASS,
       hca.ACCOUNT_ESTABLISHED_DATE    AS ACCOUNT_ESTABLISHED_DATE,
       -- Account-level profile
       acct_pc.NAME                    AS ACCOUNT_PROFILE_CLASS,
       acct_term.NAME                  AS ACCOUNT_PAYMENT_TERM,
       acct_coll.NAME                  AS ACCOUNT_COLLECTOR,
       acct_prof.CREDIT_CHECKING       AS ACCOUNT_CREDIT_CHECK,
       acct_prof.CREDIT_HOLD           AS ACCOUNT_CREDIT_HOLD,
       acct_prof.CREDIT_LIMIT          AS ACCOUNT_CREDIT_LIMIT,
       acct_prof.CREDIT_CURRENCY_CODE  AS ACCOUNT_CREDIT_CURRENCY,
       acct_prof.CREDIT_CLASSIFICATION AS ACCOUNT_CREDIT_CLASSIFICATION,
       acct_prof.RISK_CODE             AS ACCOUNT_RISK_CODE,
       -- Site and site use
       hps.PARTY_SITE_NUMBER           AS SITE_NUMBER,
       hps.PARTY_SITE_NAME             AS SITE_NAME,
       hcsu.SITE_USE_CODE              AS SITE_PURPOSE,
       hcsu.LOCATION                   AS SITE_USE_LOCATION,
       hcsu.PRIMARY_FLAG               AS PRIMARY_SITE_USE,
       su_term.NAME                    AS SITE_USE_PAYMENT_TERM,
       -- Address (HZ_LOCATIONS)
       hl.ADDRESS1                     AS ADDRESS_LINE1,
       hl.ADDRESS2                     AS ADDRESS_LINE2,
       hl.ADDRESS3                     AS ADDRESS_LINE3,
       hl.ADDRESS4                     AS ADDRESS_LINE4,
       hl.CITY                         AS CITY,
       hl.COUNTY                       AS COUNTY,
       hl.STATE                        AS STATE,
       hl.PROVINCE                     AS PROVINCE,
       hl.POSTAL_CODE                  AS POSTAL_CODE,
       hl.COUNTRY                      AS COUNTRY,
       -- Site-level profile
       site_pc.NAME                    AS SITE_PROFILE_CLASS,
       site_term.NAME                  AS SITE_PROFILE_PAYMENT_TERM,
       site_coll.NAME                  AS SITE_COLLECTOR,
       site_prof.CREDIT_HOLD           AS SITE_CREDIT_HOLD,
       site_prof.CREDIT_LIMIT          AS SITE_CREDIT_LIMIT,
       -- Site-level tax profile (ZX)
       ptp.REP_REGISTRATION_NUMBER     AS TAX_REGISTRATION_NUMBER,
       reg.REGISTRATION_NUMBER         AS DEFAULT_TAX_REGISTRATION,
       reg.TAX_REGIME_CODE             AS TAX_REGIME,
       reg.REGISTRATION_STATUS_CODE    AS TAX_REGISTRATION_STATUS,
       ptp.TAX_CLASSIFICATION_CODE     AS TAX_CLASSIFICATION,
       ptp.COUNTRY_CODE                AS TAX_COUNTRY,
       ptp.ROUNDING_RULE_CODE          AS TAX_ROUNDING_RULE,
       ptp.ROUNDING_LEVEL_CODE         AS TAX_ROUNDING_LEVEL,
       ptp.INCLUSIVE_TAX_FLAG          AS TAX_INCLUSIVE,
       ptp.PROCESS_FOR_APPLICABILITY_FLAG AS TAX_APPLICABLE,
       ptp.ALLOW_OFFSET_TAX_FLAG       AS ALLOW_OFFSET_TAX
FROM   bu
JOIN   HZ_CUST_ACCT_SITES_ALL hcas
       ON  hcas.SET_ID = bu.SITE_SET_ID
       AND hcas.STATUS = 'A'
JOIN   HZ_CUST_ACCOUNTS hca
       ON  hca.CUST_ACCOUNT_ID = hcas.CUST_ACCOUNT_ID
       AND hca.STATUS = 'A'
JOIN   HZ_PARTIES hp
       ON  hp.PARTY_ID = hca.PARTY_ID
JOIN   HZ_CUST_SITE_USES_ALL hcsu
       ON  hcsu.CUST_ACCT_SITE_ID = hcas.CUST_ACCT_SITE_ID
       AND hcsu.STATUS = 'A'
       AND hcsu.SITE_USE_CODE IN ('BILL_TO', 'SHIP_TO')
JOIN   HZ_PARTY_SITES hps
       ON  hps.PARTY_SITE_ID = hcas.PARTY_SITE_ID
JOIN   HZ_LOCATIONS hl
       ON  hl.LOCATION_ID = hps.LOCATION_ID
-- account-level profile: the profile row with no site use
LEFT JOIN HZ_CUSTOMER_PROFILES_F acct_prof
       ON  acct_prof.CUST_ACCOUNT_ID = hca.CUST_ACCOUNT_ID
       AND acct_prof.SITE_USE_ID IS NULL
       AND TRUNC(SYSDATE) BETWEEN acct_prof.EFFECTIVE_START_DATE AND acct_prof.EFFECTIVE_END_DATE
LEFT JOIN HZ_CUST_PROFILE_CLASSES acct_pc
       ON  acct_pc.PROFILE_CLASS_ID = acct_prof.PROFILE_CLASS_ID
LEFT JOIN RA_TERMS_TL acct_term
       ON  acct_term.TERM_ID = acct_prof.STANDARD_TERMS
       AND acct_term.LANGUAGE = USERENV('LANG')
LEFT JOIN AR_COLLECTORS acct_coll
       ON  acct_coll.COLLECTOR_ID = acct_prof.COLLECTOR_ID
-- site-level profile: the profile row for this site use
LEFT JOIN HZ_CUSTOMER_PROFILES_F site_prof
       ON  site_prof.SITE_USE_ID = hcsu.SITE_USE_ID
       AND TRUNC(SYSDATE) BETWEEN site_prof.EFFECTIVE_START_DATE AND site_prof.EFFECTIVE_END_DATE
LEFT JOIN HZ_CUST_PROFILE_CLASSES site_pc
       ON  site_pc.PROFILE_CLASS_ID = site_prof.PROFILE_CLASS_ID
LEFT JOIN RA_TERMS_TL site_term
       ON  site_term.TERM_ID = site_prof.STANDARD_TERMS
       AND site_term.LANGUAGE = USERENV('LANG')
LEFT JOIN AR_COLLECTORS site_coll
       ON  site_coll.COLLECTOR_ID = site_prof.COLLECTOR_ID
LEFT JOIN RA_TERMS_TL su_term
       ON  su_term.TERM_ID = hcsu.PAYMENT_TERM_ID
       AND su_term.LANGUAGE = USERENV('LANG')
-- site-level tax profile and its default registration
LEFT JOIN ZX_PARTY_TAX_PROFILE ptp
       ON  ptp.PARTY_ID = hps.PARTY_SITE_ID
       AND ptp.PARTY_TYPE_CODE = 'THIRD_PARTY_SITE'                           -- ASSUMPTION 2
LEFT JOIN ZX_REGISTRATIONS reg
       ON  reg.PARTY_TAX_PROFILE_ID = ptp.PARTY_TAX_PROFILE_ID
       AND reg.DEFAULT_REGISTRATION_FLAG = 'Y'                                -- ASSUMPTION 3
       AND TRUNC(SYSDATE) BETWEEN TRUNC(reg.EFFECTIVE_FROM) AND NVL(TRUNC(reg.EFFECTIVE_TO), TRUNC(SYSDATE))
ORDER BY hp.PARTY_NAME, hca.ACCOUNT_NUMBER, hps.PARTY_SITE_NUMBER, hcsu.SITE_USE_CODE
