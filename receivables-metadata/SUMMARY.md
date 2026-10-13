# Oracle Fusion Financials table metadata

3240 objects, 88396 columns, 3833 foreign key edges (2930 between objects in this catalog).

Source: Oracle Fusion Cloud *Tables and Views for Financials* (all tables) and *Tables and Views for Sales* (HZ_ customer tables) on docs.oracle.com, crawled with `crawler/crawl_oedmf.py`. Views, import/interface and temporary (_GT) tables are excluded. Each table file records its `source_url`, which names the release.

Flexfield columns (ATTRIBUTE*, GLOBAL_ATTRIBUTE*) are summarised per table in `flexfield_columns` rather than listed.

## Transactions

| Object | Type | Cols | Primary key | Description |
|---|---|---|---|---|
| RA_CUSTOMER_TRX_ALL | TABLE | 185 | CUSTOMER_TRX_ID | This table contains invoice, debit memo, bills receivable, and credit memo header information. Each row in this table includes general invoice information such ... |
| RA_CUSTOMER_TRX_LINES_ALL | TABLE | 197 | CUSTOMER_TRX_LINE_ID | The RA_CUSTOMER_TRX_LINES_ALL table stores line information about invoices, debit memos, credit memos, and bills receivable. For example, an invoice can have on... |
| RA_CUST_TRX_LINE_GL_DIST_ALL | TABLE | 40 | CUST_TRX_LINE_GL_DIST_ID | The RA_CUST_TRX_LINE_GL_DIST_ALL table stores the accounting records for revenue, unearned revenue, and unbilled receivables for each invoice or credit memo lin... |
| RA_CUST_TRX_LINE_SALESREPS_ALL | TABLE | 25 | CUST_TRX_LINE_SALESREP_ID | The RA_CUST_TRX_LINE_SALESREPS_ALL table stores sales credit assignments for invoice lines. If Receivables bases your invoice distributions on sales credits, a ... |
| RA_INTERFACE_LINES_ALL | missing | | | |
| AR_DEFERRED_LINES_ALL | TABLE | 20 | CUSTOMER_TRX_LINE_ID | The AR_DEFERRED_LINES_ALL table records invoice status changes, as invoices move through the revenue management life cycle. |

## Receipts and applications

| Object | Type | Cols | Primary key | Description |
|---|---|---|---|---|
| AR_CASH_RECEIPTS_ALL | TABLE | 92 | CASH_RECEIPT_ID | The AR_CASH_RECEIPTS_ALL table stores one record for each receipt that you enter. Oracle Receivables concurrently creates records in the AR_CASH_RECEIPT_HISTORY... |
| AR_CASH_RECEIPT_HISTORY_ALL | TABLE | 51 | CASH_RECEIPT_HISTORY_ID | The AR_CASH_RECEIPT_HISTORY_ALL table contains one row for each step in the life cycle of a receipt. The STATUS column indicates the status for each step: APPRO... |
| AR_RECEIVABLE_APPLICATIONS_ALL | TABLE | 92 | RECEIVABLE_APPLICATION_ID | The AR_RECEIVABLE_APPLICATIONS_ALL table stores all accounting entries for both your cash and credit memo applications. The APPLICATION_TYPE column stores eithe... |
| AR_BATCHES_ALL | TABLE | 50 | BATCH_ID | The AR_BATCHES_ALL table stores batch source information about each receipt and remittance batch. Each row includes specific batch information, such as batch so... |

## Balances, adjustments and accounting

| Object | Type | Cols | Primary key | Description |
|---|---|---|---|---|
| AR_PAYMENT_SCHEDULES_ALL | TABLE | 103 | PAYMENT_SCHEDULE_ID | The AR_PAYMENT_SCHEDULES_ALL table stores all transactions except adjustments and miscellaneous cash receipts. Oracle Receivables updates this table when activi... |
| AR_ADJUSTMENTS_ALL | TABLE | 61 | ADJUSTMENT_ID | The AR_ADJUSTMENT_ALL table stores information about your invoice adjustments. Each row includes general information about the adjustment that you make, such as... |
| AR_DISTRIBUTIONS_ALL | TABLE | 48 | LINE_ID | The AR_DISTRIBUTIONS_ALL table stores the accounting distributions for cash receipts, miscellaneous receipts, adjustments, credit memo applications, cash receip... |
| AR_CONS_INV_ALL | TABLE | 45 | CONS_INV_ID | The AR_CONS_INV_ALL table stores information about balance forward billing, including invoice numbers, customer balances, and due dates. A balance forward bill ... |
| AR_DISPUTE_HISTORY | TABLE | 14 | DISPUTE_HISTORY_ID | The AR_DISPUTE_HISTORY table stores dispute history for each payment schedule. Oracle Receivables creates a row in this table each time that the AMOUNT_IN_DISPU... |

## Setups

| Object | Type | Cols | Primary key | Description |
|---|---|---|---|---|
| RA_CUST_TRX_TYPES_ALL | TABLE | 48 | CUST_TRX_TYPE_SEQ_ID | The RA_CUST_TRX_TYPES_ALL table stores information about each transaction type used for invoices, bills receivable, and credit memos. Each row includes AutoAcco... |
| RA_BATCH_SOURCES_ALL | TABLE | 69 | BATCH_SOURCE_SEQ_ID | The RA_BATCH_SOURCES_ALL table stores information about the sources of your invoices, credit memos, and commitments. Each row includes information about invoice... |
| RA_TERMS_B | TABLE | 27 | TERM_ID | The RA_TERMS_B table stores standard payment term information. Oracle Receivables creates one row for each payment term that you define. Receivables uses this i... |
| RA_TERMS_LINES | TABLE | 17 | TERM_ID, SEQUENCE_NUM | The RA_TERMS_LINES table stores detailed line information for each payment term that you define in the RA_TERMS_B table. Oracle Receivables creates one row for ... |
| AR_RECEIPT_METHODS | TABLE | 32 | RECEIPT_METHOD_ID | The AR_RECEIPT_METHODS table contains information about receipt methods, which are receipt attributes that you define and assign to receipt classes to account f... |
| AR_RECEIPT_CLASSES | TABLE | 19 | RECEIPT_CLASS_ID | The AR_RECEIPT_CLASSES table stores user-defined receipt classes. Receipt classes determine if receipts that are assigned to a receipt class are manually or aut... |
| AR_RECEIPT_METHOD_ACCOUNTS_ALL | TABLE | 42 | RECEIPT_METHOD_ID, REMIT_BANK_ACCT_USE_ID | The AR_RECEIPT_METHOD_ACCOUNTS_ALL table is an intersection of payment methods and bank accounts. For each receipt method, every bank account that can handle th... |
| AR_BATCH_SOURCES_ALL | TABLE | 25 | BATCH_SOURCE_SEQ_ID | The AR_BATCH_SOURCES_ALL table stores information about your receipt batch sources. Receipt batch sources provide default values for the receipt class, bank acc... |
| AR_RECEIVABLES_TRX_ALL | TABLE | 29 | RECEIVABLES_TRX_ID, ORG_ID | The AR_RECEIVABLES_TRX_ALL table links distribution information with your receivables activities. Possible activity types include Adjustment, Miscellaneous Cash... |
| AR_MEMO_LINES_ALL_B | TABLE | 24 | MEMO_LINE_SEQ_ID | The AR_MEMO_LINES_ALL_B table stores information about standard memo lines for debit memos, on-account credits, debit memo reversals, chargebacks, and invoices.... |
| AR_SYSTEM_PARAMETERS_ALL | TABLE | 159 | ORG_ID | AR_SYSTEM_PARAMETERS_ALL contains customizations to Oracle Fusion Receivables. This table stores installation-wide options. At least one row must always exist i... |
| AR_AGING_BUCKETS | TABLE | 15 | AGING_BUCKET_ID | Stores information about the aging buckets. For example, define an aging bucket called Old Past Due Items that includes an aging bucket line for invoices that a... |
| AR_AGING_BUCKET_LINES_B | TABLE | 18 | AGING_BUCKET_LINE_ID | This table stores the line level detail for aging buckets. |
| AR_COLLECTORS | TABLE | 20 | COLLECTOR_ID | The stage sequence associated to a payment schedule. |
| AR_LOOKUPS | missing | | | |

## Customers (TCA)

| Object | Type | Cols | Primary key | Description |
|---|---|---|---|---|
| HZ_CUST_ACCOUNTS | TABLE | 41 | CUST_ACCOUNT_ID | The HZ_CUST_ACCOUNTS table stores information about customer accounts , or business relationships that the deploying company establishes with a party of type Or... |
| HZ_PARTIES | TABLE | 96 | PARTY_ID | The HZ_PARTIES table stores basic information about parties. Although a record in the HZ_PARTIES table represents a unique party, multiple parties can have the ... |
| HZ_CUST_ACCT_SITES_ALL | TABLE | 32 | CUST_ACCT_SITE_ID | The HZ_CUST_ACCT_SITES_ALL table stores all customer account sites across all operating units. Customer account sites are customer account addresses with which ... |
| HZ_CUST_SITE_USES_ALL | TABLE | 41 | SITE_USE_ID | The HZ_CUST_SITE_USES_ALL table stores business purposes assigned to customer account sites, for example Bill-To, Ship-To, and Statements. Each customer account... |
| HZ_PARTY_SITES | TABLE | 43 | PARTY_SITE_ID | The HZ_PARTY_SITES table stores all the addresses associated to a party. If the address does not exist as a location, then a new location is created and the ass... |
| HZ_LOCATIONS | TABLE | 63 | LOCATION_ID | The HZ_LOCATIONS table stores information about a delivery or postal address such as building number, street address, postal code, and directions to a location.... |

## Other objects (3206)

| Object | Type | Cols | Description |
|---|---|---|---|
| AP_1096_DATA_ALL | TABLE | 12 | AP_1096_DATA_ALL contains summary payment information for 1099 type suppliers. The Internal Revenue ... |
| AP_1099G_DATA_ALL | TABLE | 15 | AP_1099G_DATA_ALL contains 1099 supplier payment totals made for Certain Government Payments. The 10... |
| AP_1099_TAPE_DATA_ALL | TABLE | 40 | AP_1099_TAPE_DATA_ALL is a temporary table that holds 1099 supplier payment totals used for creating... |
| AP_AGING_PERIODS | TABLE | 13 | AP_AGING_PERIODS contains aging periods that you define for use in the Invoice Aging Report. You nee... |
| AP_AGING_PERIOD_LINES | TABLE | 18 | AP_AGING_PERIOD_LINES contains information on individual aging periods. The Invoice Aging Report ret... |
| AP_ALLOCATION_RULES | TABLE | 17 | AP_ALLOCATION_RULES contains records establishing how charge lines (Freight and Miscellaneous) shoul... |
| AP_ALLOCATION_RULE_LINES | TABLE | 17 | AP_ALLOCATION_RULE_LINES contains the records that establish which percentage and/or amount of a cha... |
| AP_APINV_APPROVERS | TABLE | 44 | This table connects approvers to their invoice components, either the invoice header or the invoice ... |
| AP_AWT_BUCKETS_ALL | TABLE | 18 | AP_AWT_BUCKETS_ALL contains the denormalized amount of tax withheld to date for a particular supplie... |
| AP_AWT_GROUPS | TABLE | 10 | AP_AWT_GROUPS contains withholding tax groups. Each withholding tax group contains one or more withh... |
| AP_AWT_GROUP_TAXES_ALL | TABLE | 11 | AP_AWT_GROUP_TAXES_ALL is the intersection table that belongs to a specific withholding tax group an... |
| AP_AWT_TAX_RATES_ALL | TABLE | 22 | AP_AWT_TAX_RATES_ALL contains tax rates for Withholding tax type tax codes. Oracle Payables predefin... |
| AP_AWT_TEMP_DISTRIBUTIONS_ALL | TABLE | 24 | AP_AWT_TEMP_DISTRIBUTIONS_ALL contains temporary withholding tax type invoice distributions for proj... |
| AP_BANK_CHARGES | TABLE | 20 | AP_BANK_CHARGES contains header information that you enter on the bank charges page. A bank charge i... |
| AP_BANK_CHARGE_LINES | TABLE | 14 | AP_BANK_CHARGE_LINES contains ranges for bank charges. A record is uniquely identified by the BANK_C... |
| AP_BATCHES_ALL | TABLE | 25 | AP_BATCHES_ALL contains summary information about invoices you enter in batches if you enable the Ba... |
| AP_CHECKS_ALL | TABLE | 129 | AP_CHECKS_ALL stores information about payments issued to suppliers or refunds received from supplie... |
| AP_CORRELATION_SEQ_ACCT_DATES | TABLE | 12 | AP_CORRELATION_SEQ_ACCT_DATES contains the maximum accounting date of transactions with a document s... |
| AP_CURRENCY_GROUP | TABLE | 10 | This table has been created to allow the user to select multiple values for the payment currencies f... |
| AP_DISCOUNT_NOTIFICATIONS | TABLE | 14 | This table contains information about the discount offer notifications sent to the supplier and the ... |
| AP_DISCOUNT_NOTIFICATION_INFO | TABLE | 10 | This table contains details of the invoices sent along with the discount offer notification. |
| AP_DISCOUNT_OFFERS_ASSIGN | TABLE | 23 | This table contains information about the supplier assigned to the discount offer. |
| AP_DISCOUNT_OFFERS_B | TABLE | 14 | This table contains discount offers. |
| AP_DISCOUNT_OFFERS_TL | TABLE | 11 | This table contains translated discount offers. |
| AP_DISTRIBUTION_SETS_ALL | TABLE | 12 | AP_DISTRIBUTION_SETS_ALL contains information about Distribution Sets you define to distribute invoi... |
| AP_DISTRIBUTION_SET_LINES_ALL | TABLE | 52 | AP_DISTRIBUTION_SET_LINES_ALL contains detailed information about individual distribution lines you ... |
| AP_DOCIO_STREAM_DETAILS | TABLE | 45 | This table contains the summary and status information for all Payables documents ingested through v... |
| AP_DOC_SEQUENCE_AUDIT | TABLE | 9 | AP_DOC_SEQUENCES_AUDIT contains audit information for document sequence numbers assigned to invoices... |
| AP_HISTORY_CHECKS_ALL | TABLE | 18 | AP_HISTORY_CHECKS_ALL contains summary information on invoice payments your Oracle Payables applicat... |
| AP_HISTORY_INVOICES_ALL | TABLE | 18 | AP_HISTORY_INVOICES_ALL stores summary information of the invoices your Oracle Payables application ... |
| AP_HISTORY_INV_PAYMENTS_ALL | TABLE | 10 | AP_HISTORY_INVOICE_PAYMENTS_ALL stores the relationship between invoices and payments that your Orac... |
| AP_HOLDS_ALL | TABLE | 25 | AP_HOLDS_ALL contains information about holds that you or your Oracle Payables application place on ... |
| AP_HOLD_CODES | TABLE | 20 | AP_HOLD_CODES contains information about hold codes and release codes that you or your Oracle Payabl... |
| AP_IDR_OPTIONS | TABLE | 34 | AP_IDR_OPTIONS contains the parameters and defaults you define for operating your Intelligent Docume... |
| AP_IDR_OPTION_EXTENSIONS | TABLE | 12 | This table contains information about the additional configuration options listed under the IDR Opti... |
| AP_INCOME_TAX_REGIONS | TABLE | 32 | AP_INCOME_TAX_REGIONS contains information about the tax regions you use to record payment informati... |
| AP_INCOME_TAX_TYPES | TABLE | 12 | AP_INCOME_TAX_TYPES stores the 1099-MISC types that you can assign to a supplier for 1099 reporting.... |
| AP_INTEREST_PERIODS | TABLE | 10 | AP_INTEREST_PERIODS contains information about interest rates and periods that Payables uses to crea... |
| AP_INVOICES_ALL | TABLE | 182 | AP_INVOICES_ALL contains records for invoices you enter. There is one row for each invoice youenter.... |
| AP_INVOICE_DISTRIBUTIONS_ALL | TABLE | 194 | AP_INVOICE_DISTRIBUTIONS_ALL holds the distribution information that is manually entered or system-g... |
| AP_INVOICE_KEY_IND_ALL | TABLE | 45 | AP_INVOICE_KEY_IND stores compiled invoice information for the Key Indicators Report. There is one r... |
| AP_INVOICE_LINES_ALL | TABLE | 210 | AP_INVOICE_LINES_ALL contains records for invoice lines entered manually, generated automatically or... |
| AP_INVOICE_PAYMENTS_ALL | TABLE | 66 | AP_INVOICE_PAYMENTS_ALL contains records of invoice payments that you made to suppliers. There is on... |
| AP_INVOICE_RELATIONSHIPS | TABLE | 10 | AP_INVOICE_RELATIONSHIPS relates records in AP_INVOICES_ALL with one another to match Interest invoi... |
| AP_INV_APRVL_HIST_ALL | TABLE | 28 | AP_INV_APRVL_HIST_ALL contains the approval and rejection history of each invoice that passes throug... |
| AP_INV_SELECTION_CRITERIA_ALL | TABLE | 68 | AP_INVOICE_SELECTION_CRITERIA_ALL stores the criteria that a payment batch uses to select invoices f... |
| AP_LE_GROUP | TABLE | 10 | This table has been created to allow the user to select multiple values for legal entities for the P... |
| AP_MATCHING_RULES | TABLE | 11 | AP_MATCHING_RULES table contains the rule information to perform automatic matching of invoice lines... |
| AP_MATCHING_RULE_ATTRS | TABLE | 10 | AP_MATCHING_RULE_ATTRS table contains the matching attribute information for a matching rule. |
| AP_MATCHING_RULE_SETS | TABLE | 10 | AP_MATCHING_RULE_SETS table contains the rule set information to perform automatic matching of invoi... |
| AP_MATCHING_RULE_SET_LINES | TABLE | 11 | AP_MATCHING_RULE_SET_LINES contains matching rule information for a matching rule set. |
| AP_NEGOTIATION_HIST | TABLE | 12 | AP_NEGOTIATION_HIST contains the information changed by the approver or supplier when negotiating an... |
| AP_OTHER_PERIODS | TABLE | 18 | AP_OTHER_PERIODS contains information about the time periods you define for use in recurring invoice... |
| AP_OTHER_PERIOD_TYPES | TABLE | 15 | AP_OTHER_PERIOD_TYPES stores the period type you define and use to create recurring invoice, automat... |
| AP_OU_GROUP | TABLE | 10 | This table has been created to allow the user to select multiple values for the operating units for ... |
| AP_PAYMENT_HISTORY_ALL | TABLE | 62 | AP_PAYMENT_HISTORY_ALL stores the clearing/unclearing history for payments. It also stores the matur... |
| AP_PAYMENT_HIST_DISTS | TABLE | 40 | The APHD table is populated during the pre-processing of the accounting extract that occurs when the... |
| AP_PAYMENT_KEY_IND_ALL | TABLE | 39 | AP_PAYMENT_KEY_IND stores compiled payment information for the Key Indicators Report. There is one r... |
| AP_PAYMENT_SCHEDULES_ALL | TABLE | 49 | AP_PAYMENT_SCHEDULES_ALL contains information about scheduled payments for an invoice. You need one ... |
| AP_PAYMENT_TEMPLATES | TABLE | 52 | The AP_PAYMENT_TEMPLATES table contains the user defined Payment Process Request Templates. The Temp... |
| AP_PAY_GROUP | TABLE | 10 | This table has been created to allow the user to select multiple values for the pay groups for the P... |
| AP_PPR_MULTI_SELECT_CRITERIA | TABLE | 13 | Used for multiple PPR selection criteria. |
| AP_PREPAY_APP_DISTS | TABLE | 45 | This table details the distribution of prepayment application invoice distributions to the recipient... |
| AP_PREPAY_HISTORY_ALL | TABLE | 27 | AP_PREPAY_HISTORY_ALL countains the history of a prepayment which includes its related prepayment ap... |
| AP_PRODUCT_REGISTRATIONS | TABLE | 15 | ***** Warning: Oracle Internal Use Only ***** Oracle Corporation does not support access to Oracle a... |
| AP_RECON_DIFFERENCE_DETAILS | TABLE | 17 | This table contains the details of the transactions causing the difference while reconciling Oracle ... |
| AP_RECON_SUMMARY_CCID | TABLE | 14 | This table stores the Payable CCIDs for a given Request_ID. The CCIDs are derived from the from and ... |
| AP_RECON_SUMMARY_DETAILS | TABLE | 20 | This table stores the extract of the data, which is required for the preparation of the summary repo... |
| AP_RECON_SUMMARY_PARAMETERS | TABLE | 25 | This table stores the parameters input by the user for executing the Data Extraction Program. |
| AP_REPORTING_ENTITIES_ALL | TABLE | 11 | AP_REPORTING_ENTITIES_ALL contains information about the reporting entities you define for 1099 repo... |
| AP_REPORTING_ENTITY_LINES_ALL | TABLE | 9 | AP_REPORTING_ENTITY_LINES_ALL holds the line information for the tax reporting entities you define. ... |
| AP_SELECTED_INVOICES_ALL | TABLE | 96 | AP_SELECTED_INVOICES_ALL is a temporary table that stores information about invoices selected for pa... |
| AP_SELF_ASSESSED_TAX_DIST_ALL | TABLE | 167 | AP_SELF_ASSESSED_TAX_DIST contains self assessed tax distributions |
| AP_SOURCE_GROUP | TABLE | 10 | This table contains the source group selection criteria information for the Payment Process Request ... |
| AP_STATEMENT_HEADERS | TABLE | 49 | This table contains information about the statement headers. test |
| AP_STATEMENT_IMPORT_ERRORS | TABLE | 12 | This table contains information about the statement import errors. |
| AP_STATEMENT_LINES | TABLE | 101 | This table contains information about the statement lines. |
| AP_SUPPLIER_BALANCE_ITF | TABLE | 38 | This is an interface table that stores all the records for the submission of the AP Supplier Open Ba... |
| AP_SYSTEM_PARAMETERS_ALL | TABLE | 121 | AP_SYSTEM_PARAMETERS_ALL contains the parameters and defaults you define for operating your Oracle P... |
| AP_TAX_CODES_ALL | TABLE | 30 | AP_TAX_CODES_ALL contains information about the tax codes you define. You need one row for each tax ... |
| AP_TERMS_B | TABLE | 16 | AP_TERMS_B stores header information about payment terms you define. You need one row for each type ... |
| AP_TERMS_LINES | TABLE | 30 | AP_TERMS_LINES stores detail information about payment terms you define. You need one row for each s... |
| AP_TERMS_ST | TABLE | 11 | AP_TERMS_ST stores set id information for the payment terms you define. |
| AP_TERMS_TL | TABLE | 14 | AP_TERMS stores header information about payment terms you define. You need one row for each type of... |
| AP_TOLERANCE_TEMPLATES | TABLE | 22 | AP_TOLERANCE_TEMPLATES contains the tolerance levels you set for matching and invoice variance testi... |
| AP_TRIAL_BALANCES | TABLE | 28 | This table stores trial balance information |
| AP_TRIAL_BAL_LOGS | TABLE | 15 | This table stores trial balance logging information |
| AP_UNSELECTED_INVOICES_ALL | TABLE | 11 | AP_UNSELECTED_INVOICES_ALL is a temporary table used for payment batches. It holds invoice records i... |
| AP_USER_EXCHANGE_RATES | TABLE | 13 | This table holds User type exchange rate when submitting the payment process request for multiple cu... |
| AP_VENDOR_KEY_IND_ALL | TABLE | 27 | Compiled supplier information for the Key Indicators Report |
| AP_WHT_ITF | TABLE | 85 | This is an interface table that stores all the records for the submission of the AP Withholding Tax ... |
| ARB_PAYMENT_AUDIT | TABLE | 23 | This table stores a record for each payment requested through Bill Management. |
| ARB_PREFERENCE_ITEMS | TABLE | 12 | This table contains bill management preference items |
| ARB_REG_ACCESS_DETAILS | TABLE | 11 | This table stores the details of customer account or site access requests for a Bill Management user... |
| ARB_REG_ACCESS_REQUESTS | TABLE | 10 | This table stores the status of the customer account or site access requests for a Bill Management u... |
| ARB_REG_LDAP_REQUESTS | TABLE | 14 | This table stores the LDAP user request details and status of Bill Management. |
| ARB_REG_PROVISIONABLE_ROLES | TABLE | 8 | This table stores data for the provisionable role configuration of Bill Management, such as whether ... |
| ARB_REG_ROLE_REQUESTS | TABLE | 12 | This table stores the LDAP user role request details and status of Bill Management. |
| ARB_REG_USER_PROFILES | TABLE | 20 | This table stores the Bill Management user information provided during registration. |
| ARB_SYSTEM_PARAMETERS | TABLE | 23 | The ARB_SYSTEM_PARAMETERS table contains customizations to Oracle Fusion Bill Management. This table... |
| AR_ACTIVITY_DETAILS | TABLE | 30 | This is an obsolete table and not in use. |
| AR_AGING_BUCKET_LINES_TL | TABLE | 15 | Aging bucket lines translated table. |
| AR_AGING_EXTRACT | TABLE | 44 | AR_AGING_EXTRACT is a staging table that contains aging balances of the payment schedule records sel... |
| AR_AGING_MFAR_EXTRACT | TABLE | 16 | AR_AGING_MFAR_EXTRACT is a staging table that contains aging balances by Receivables balancing segme... |
| AR_AGING_PAYMENT_SCHEDULES | TABLE | 11 | AR_AGING_PAYMENT_SCHEDULES is a staging table that contains the payment schedule records selected du... |
| AR_APPROVAL_ACTION_HISTORY | TABLE | 12 | The AR_APPROVAL_ACTION_HISTORY table stores information about each step in the life cycle of an adju... |
| AR_APPROVAL_USER_LIMITS | TABLE | 16 | The AR_APPROVAL_USER_LIMITS table stores information about each approval limit, for each currency, w... |
| AR_APP_EXCEPTION_RULES | TABLE | 16 | This table stores the header level information on Over/Under Payment Rules |
| AR_APP_EXCEPTION_RULE_DTLS | TABLE | 18 | This table stores the line level information on Over/Under Payment Rules |
| AR_APP_RULES | TABLE | 14 | The AR_APP_RULES table stores information about individual application rules within an application r... |
| AR_APP_RULE_DETAILS | TABLE | 14 | The AR_APP_RULE_DETAILS table stores detailed information about an application rule, including amoun... |
| AR_APP_RULE_SETS | TABLE | 15 | The AR_APP_RULE_SETS table contains information for each application rule set defined. Application r... |
| AR_AUTOCASH_HIERARCHIES | TABLE | 20 | The AR_AUTOCASH_HIERARCHIES table stores information about each AutoCash rule set that you define. E... |
| AR_AUTOCASH_RULES | TABLE | 14 | The AR_AUTOCASH_RULES table stores information about each AutoCash Rule in an AutoCash Rule Set. Eac... |
| AR_AUTOMATCH_RULES | TABLE | 29 | This table stores the header level information on the Automatch rules |
| AR_AUTOMATCH_RULE_DTLS | TABLE | 13 | This table stores the line level information on the Automatch Rules |
| AR_AUTOMATCH_TRX_T | TABLE | 83 | This table stores the processing data for the Automatch Process |
| AR_AUTOREC_EXCEPTIONS | TABLE | 24 | The AR_AUTOREC_EXCEPTIONS table is a temporary table used to store exceptions found by Automatic Rec... |
| AR_AUTOREC_INTERIM | TABLE | 20 | The AR_AUTOREC_INTERIM table is a temporary table used for parallel processing of automatic receipts... |
| AR_BANK_STMT_REFERENCE_TAGS | TABLE | 12 | Stores structured reference tags extracted from bank statement addenda text for each bank account. T... |
| AR_BASE_GL_ACCT_BALANCES | TABLE | 22 | This is an obsolete table and not in use. |
| AR_BILLREV_ACTIVITY_DETAILS | TABLE | 17 | This is an obsolete table and not in use. |
| AR_BILL_REVENUE_RECONCILIATION | TABLE | 22 | This table is used for Billing and Revenue reconciliation. It is for future use only. |
| AR_BPA_AREA_ITEMS | TABLE | 15 | This is an obsolete table and not in use. |
| AR_BPA_CONTENT_AREAS_B | TABLE | 38 | This is an obsolete table and not in use. |
| AR_BPA_CONTENT_AREAS_TL | TABLE | 12 | This is an obsolete table and not in use. |
| AR_BPA_DATASRC_APPS_B | TABLE | 11 | This is an obsolete table and not in use. |
| AR_BPA_DATASRC_APPS_TL | TABLE | 11 | This is an obsolete table and not in use. |
| AR_BPA_DATA_SOURCES_B | TABLE | 20 | This is an obsolete table and not in use. |
| AR_BPA_DATA_SOURCES_TL | TABLE | 11 | This is an obsolete table and not in use. |
| AR_BPA_DATA_SRC_PARAMS | TABLE | 13 | This is an obsolete table and not in use. |
| AR_BPA_DELIVERY_DETAILS | TABLE | 20 | The AR_BPA_DELIVERY_DETAILS stores information that is used for delivering printed transactions via ... |
| AR_BPA_ITEMS_B | TABLE | 28 | This is an obsolete table and not in use. |
| AR_BPA_ITEMS_TL | TABLE | 13 | This is an obsolete table and not in use. |
| AR_BPA_PAGE_SETUPS_B | TABLE | 18 | This is an obsolete table and not in use. |
| AR_BPA_PAGE_SETUPS_TL | TABLE | 11 | This is an obsolete table and not in use. |
| AR_BPA_PRINT_REQUESTS | TABLE | 15 | This is an obsolete table and not in use. |
| AR_BPA_RULES_B | TABLE | 19 | This is an obsolete table and not in use. |
| AR_BPA_RULES_TL | TABLE | 11 | This is an obsolete table and not in use. |
| AR_BPA_RULE_ATTRIBUTES_B | TABLE | 10 | This is an obsolete table and not in use. |
| AR_BPA_RULE_ATTRIBUTES_TL | TABLE | 10 | This is an obsolete table and not in use. |
| AR_BPA_RULE_TEMPLATES | TABLE | 12 | This is an obsolete table and not in use. |
| AR_BPA_TEMPLATES_B | TABLE | 39 | This is an obsolete table and not in use. |
| AR_BPA_TEMPLATES_TL | TABLE | 11 | This is an obsolete table and not in use. |
| AR_BPA_TEMPLATE_FIELDS | TABLE | 10 | This is an obsolete table and not in use. |
| AR_BPA_TEMPLATE_FILES | TABLE | 11 | This is an obsolete table and not in use. |
| AR_BR_TRX_BATCH_RPT | TABLE | 26 | AR_BR_TRX_BATCH_RPT table contains data populated by the Create Automatic Bills Receivable Batch pro... |
| AR_CASH_EXCEPTION_TRENDS_ALL | TABLE | 12 | This table is used to store the exception reasons of applying the transaction manually. |
| AR_CASH_PROCESSING_EXCEPTIONS | TABLE | 29 | This table contains error information resulting from cash processing documents. |
| AR_CASH_RECOS_ALL | TABLE | 45 | This table stores the header information of the recommendations on a receipt reference |
| AR_CASH_RECO_LINES_ALL | TABLE | 24 | This table stores the line information of the recommendations on a receipt reference |
| AR_CASH_REMIT_REFS_ALL | TABLE | 54 | This table stores the references on a receipt |
| AR_CCID_BY_GL_ACCOUNTS | TABLE | 8 | This is an obsolete table and not in use. |
| AR_CC_ERROR_HISTORY | TABLE | 20 | Whenever a transaction has a credit card error that has been marked for automatic correction, the AR... |
| AR_CC_ERROR_MAPPINGS | TABLE | 22 | The AR_CC_ERROR_MAPPINGS table contains the mapping between credit card errors and their correspondi... |
| AR_CHARGE_SCHEDULES | TABLE | 9 | The AR_CHARGE_SCHEDULES table contains information for late charge schedules. |
| AR_CHARGE_SCHEDULE_HDRS | TABLE | 13 | The AR_CHARGE_SCHEDULE_HDRS table contains header information for late charges schedules. |
| AR_CHARGE_SCHEDULE_LINES | TABLE | 13 | The AR_CHARGE_SCHEDULE_LINES table contains line information for late charges schedules. |
| AR_CLOSED_GL_PERIODS | TABLE | 10 | This is an obsolete table and not in use. |
| AR_CMGT_APPROVAL_HISTORY | TABLE | 11 | This table contains the approval history of credit case folders. |
| AR_CMGT_CASE_FOLDERS | TABLE | 51 | This table contains the credit case folders. |
| AR_CMGT_CF_DTLS | TABLE | 17 | This table contains the credit case folder details. |
| AR_CMGT_CF_RECOMMENDS | TABLE | 12 | This table contains the recommendations in credit case folders. |
| AR_CMGT_CF_TEMPLATE | TABLE | 19 | This table contains the credit case folder templates, used during new case folder creation. |
| AR_CMGT_CF_TEMPLATE_DTLS | TABLE | 13 | This table contains the credit case folder template details. |
| AR_CMGT_DATA_POINTS_B | TABLE | 20 | This table contains the predefined credit data points. |
| AR_CMGT_DATA_POINTS_TL | TABLE | 14 | This table contains the translated predefined credit data points. |
| AR_CMGT_SCORES | TABLE | 14 | This table contains the credit scoring models defined based on data points. Credit scoring models ar... |
| AR_CMGT_SCORE_DTLS | TABLE | 10 | This table contains the data points and weights in credit scoring models. |
| AR_CMGT_SCORE_RANGE | TABLE | 17 | This table contains the data point ranges and scores in credit scoring models. |
| AR_CONC_PROCESS_REQUESTS | TABLE | 7 | The AR_CONC_PROCESS_REQUESTS table contains a list of Oracle Receivables AutoInvoice and Customer Me... |
| AR_CONFIRMATION_ACTIONS | TABLE | 13 | This table stores information about which action to take based on the information that is included i... |
| AR_CONS_BILLING_SETS_ALL | TABLE | 14 | This table stores details of billing sets assigned to consolidation entity documents, indicating the... |
| AR_CONS_BILLING_TERMS_B | TABLE | 13 | This table contains the billing terms used to consolidate lines from various source systems into an ... |
| AR_CONS_BILLING_TERMS_TL | TABLE | 11 | This table provides multilingual support for each of the Consolidation Billing terms. It allows stor... |
| AR_CONS_BILL_CYCLES_B | TABLE | 58 | The AR_CONS_BILL_CYCLES_B table stores information on defined cycles. Receivables creates one row fo... |
| AR_CONS_BILL_CYCLES_TL | TABLE | 14 | The AR_CONS_BILL_CYCLES_TL table provides multilingual support for each billing cycle that you defin... |
| AR_CONS_BILL_CYCLE_DATES | TABLE | 8 | This table stores billing dates for given billing cycle. |
| AR_CONS_BILL_TERM_BATCH_SRC | TABLE | 9 | This table contains a list of transaction sources that should be considered while generating a conso... |
| AR_CONS_BILL_TERM_EXCLUSIONS | TABLE | 10 | This table contains a list of exclusions that should be considered while generating a consolidated i... |
| AR_CONS_INV_TRX_ALL | TABLE | 21 | The AR_CONS_INV_TRX_ALL table contains header-level information about transactions that are included... |
| AR_CONS_INV_TRX_LINES_ALL | TABLE | 19 | The AR_CONS_INV_TRX_LINES_ALL table contains information about transaction lines on a balance forwar... |
| AR_CREATE_RECEIPTS_ERROR | TABLE | 22 | This table contains errors resulting from unsuccessful attempts by the bulk receipts creation API. |
| AR_CREDIT_HISTORIES | TABLE | 20 | The AR_CREDIT_HISTORIES table stores information about a customer's credit profile or changes made t... |
| AR_CREDIT_MEMO_AMOUNTS | TABLE | 14 | The AR_CREDIT_MEMO_AMOUNTS table stores the amount of revenue reduction that is recognized when you ... |
| AR_CUSTOMER_ALT_NAMES | TABLE | 17 | The AR_CUSTOMER_ALT_NAMES table contains alternate customer names that are often used by Japanese bu... |
| AR_CUSTOMER_BALANCE_ITF | TABLE | 35 | Customers selected for the Customer Open Balance letter report |
| AR_CUSTOMER_REFERENCE_MAPPINGS | TABLE | 14 | Maintains mapping records between canonical objects and their associated extension fields, including... |
| AR_CUST_CREDIT_AUTHORIZATION | TABLE | 24 | This entity describes credit amounts that have been authorized for a customer account. |
| AR_CUST_OPEN_AUTH_SUMMARY | TABLE | 9 | This table stores information about the open authorization amount for a customer account. |
| AR_CUST_UPD_BATCH_HISTORY | TABLE | 12 | AR_CUST_UPD_BATCH_HISTORY contains historical information about customer upload batches. |
| AR_CUST_UPD_BATCH_SUMMARY | TABLE | 16 | AR_CUST_UPD_BATCH_SUMMARY contains summary information about customer upload batches. |
| AR_CUST_UPD_ERRMSG_MAP | TABLE | 25 | AR_CUST_UPD_ERRMSG_MAP contains mapping information for error messages raised during the customer bu... |
| AR_DEFERRAL_REASONS | TABLE | 21 | The AR_DEFERRAL_REASONS table contains both seeded and user-defined revenue contingency definitions. |
| AR_DETAILED_DISTRIBUTIONS_ALL | TABLE | 46 | This table contains the prorated detailed accounting distributions derived from the AR_DISTRIBUTIONS... |
| AR_DISTRIBUTION_SETS_ALL | TABLE | 12 | The AR_DISTRIBUTION_SETS_ALL table stores general information about your distribution sets, such as ... |
| AR_DISTRIBUTION_SET_LINES_ALL | TABLE | 13 | The AR_DISTRIBUTION_SET_LINES_ALL table stores specific information, such as GL account information,... |
| AR_DOCUMENT_TRANSFERS | TABLE | 36 | This is an obsolete table and not in use. |
| AR_DOC_SEQUENCE_AUDIT | TABLE | 9 | The AR_DOC_SEQUENCE_AUDIT table stores a row for every document number that is generated. Document s... |
| AR_DOC_TRANSFER_CUSTOMER_EXT | TABLE | 213 | This is a temporary table which is used internally by Oracle. The AR_DOC_TRANSFER_CUSTOMER_EXT table... |
| AR_DOC_TRANSFER_HEADER_EXT | TABLE | 124 | This is a temporary table which is used internally by Oracle. The AR_DOC_TRANSFER_HEADER_EXT table s... |
| AR_DOC_TRANSFER_LINE_EXT | TABLE | 49 | This is a temporary table which is used internally by Oracle. The AR_DOC_TRANSFER_LINE_EXT table sto... |
| AR_EXTENSION_ATTRIBUTES | TABLE | 13 | This table contains the extension attribute name value pairs that a user can add to Accounts Receiva... |
| AR_GL_ACCT_BALANCES | TABLE | 22 | This is an obsolete table and not in use. |
| AR_INCOMPLETE_TRX_HIST | TABLE | 11 | Stores incomplete transaction history for receivables dashboard page |
| AR_INTEREST_BATCHES_ALL | TABLE | 14 | The AR_INTEREST_BATCHES_ALL table contains the batch information for late charges. |
| AR_INTEREST_HEADERS_ALL | TABLE | 55 | The AR_INTEREST_HEADERS_ALL table contains header level late charge document information. |
| AR_INTEREST_LINES_ALL | TABLE | 33 | The AR_INTEREST_LINES_ALL table contains line level late charge document information. |
| AR_INTERIM_CASH_RCPT_LINES_ALL | TABLE | 30 | The AR_INTERIM_CASH_RCPT_LINES_ALL table is a temporary table that stores entries for unposted recei... |
| AR_INTERIM_CASH_RECEIPTS_ALL | TABLE | 61 | The AR_INTERIM_CASH_RECEIPTS_ALL table is a temporary table that stores entries for receipt batches ... |
| AR_JOURNAL_INTERIM_ALL | TABLE | 97 | Temporary table used by the Journal Entries report |
| AR_LATE_CHARGE_TRX_T | TABLE | 46 | Table which stores the eligible transactions for late charge processing |
| AR_LC_CUST_SITES_T | TABLE | 47 | Table which stores the eligible customers for late charge processing |
| AR_LINE_CONTS_ALL | TABLE | 19 | The AR_LINE_CONTS_ALL table stores, for each line, contingencies that impact revenue. |
| AR_LOCKBOXES_ALL | TABLE | 35 | The AR_LOCKBOXES_ALL table contains information about your Lockboxes. Lockbox is a service commercia... |
| AR_MEMO_LINES_ALL_TL | TABLE | 15 | The AR_MEMO_LINES_ALL_TL table provides multilingual support for standard memo lines that you define... |
| AR_MISC_CASH_DISTRIBUTIONS_ALL | TABLE | 36 | The AR_MISC_CASH_DISTRIBUTIONS_ALL table stores all accounting entries for your miscellaneous cash a... |
| AR_NOTES | TABLE | 13 | This table is used when correcting credit card errors raised for the transaction by the Automatic Re... |
| AR_PAY_REL_ASSIGNMENTS | TABLE | 13 | This table stores assignments between an existing customer hierarchy type (or tree structure) to one... |
| AR_PERIODS | TABLE | 13 | Information about accounting periods |
| AR_PERIOD_TYPES | TABLE | 9 | Information about accounting period types |
| AR_PMT_SCHEDULE_PREDICTIONS | TABLE | 12 | The AR_PMT_SCHEDULE_PREDICTIONS table stores the customer payment prediction information for a payme... |
| AR_RAMC_AUDIT_TRAIL | TABLE | 37 | The AR_RAMC_AUDIT_TRAIL table records status changes for invoices as it goes through the revenue man... |
| AR_RATE_ADJUSTMENTS_ALL | TABLE | 24 | The AR_RATE_ADJUSTMENTS_ALL table stores information about currency exchange rate adjustments. Oracl... |
| AR_RCPT_RVRSL_MPNGS | TABLE | 11 | The AR_RCPT_RVRSL_MPNGS_ALL table stores the reversal mappings between REVERSAL_REASON_CODE and REVE... |
| AR_RECON_DIFFERENCE_DETAILS | TABLE | 17 | This table contains the details of the transactions causing the difference while reconciling Oracle ... |
| AR_RECON_SUMMARY_CCID | TABLE | 14 | This table contains the Receivable general ledger account code combination for a given scheduled pro... |
| AR_RECON_SUMMARY_DETAILS | TABLE | 20 | This table stores the extract of the data, which is required for the preparation of the summary repo... |
| AR_RECON_SUMMARY_PARAMETERS | TABLE | 26 | This table stores the parameters input by the user for executing the Data Extraction Program. |
| AR_REC_TRX_LE_DETAILS_ALL | TABLE | 11 | Stores the asset and liability tax_rate_codes by legal entity for each receivable activity. |
| AR_REF_ACCOUNTS_ALL | TABLE | 23 | This table stores reference account information for various entities, including transaction types, s... |
| AR_REMITTANCE_ADVICES_ALL | TABLE | 43 | This table stores the receipt header information from remittance advices. |
| AR_REMIT_TO_LOCS_ALL | TABLE | 10 | This table stores Remit-to address locations. |
| AR_REVENUE_ADJUSTMENTS_ALL | TABLE | 35 | The AR_REVENUE_ADJUSTMENTS_ALL table stores all information about revenue adjustments on transaction... |
| AR_REVENUE_EVENTS_TMP | TABLE | 3 | STORES THE REVENUE EVENTS BASED ON BUSINESS UNIT |
| AR_REV_ADJ_TEMP_ALL | TABLE | 112 | Temporary Table to hold the Data while doing Revenue Adjustment Transactions |
| AR_SALES_CREDIT_TYPES | TABLE | 16 | The AR_SALES_CREDIT_TYPES table contains information about seeded sales credit types Quota Sales Cre... |
| AR_SELECTION_CRITERIA | TABLE | 20 | AR_SELECTION_CRITERIA contains the selection criteria that are used by the Create Automatic Bills Re... |
| AR_STANDARD_TEXT_B | TABLE | 13 | The AR_STANDARD_TEXT_B table contains user defined standard messages that are optionally selected to... |
| AR_STANDARD_TEXT_TL | TABLE | 10 | The AR_STANDARD_TEXT_TL table contains multilingual support for standard text messages that you defi... |
| AR_STATEMENTS_HISTORY_ALL | TABLE | 25 | The history of every customer statement that you generate |
| AR_STATEMENT_CYCLES | TABLE | 17 | The AR_STATEMENT_CYCLES table contains general information about each statement cycle such as the in... |
| AR_STATEMENT_CYCLE_DATES_ALL | TABLE | 16 | The AR_STATEMENT_CYCLE_DATES_ALL table contains the dates that you specify for a statement cycle to ... |
| AR_STATEMENT_CYCLE_INTERVALS | TABLE | 12 | The AR_STATEMENT_CYCLE_INTERVALS table contains statement cycle intervals. Cycle intervals are the s... |
| AR_STATEMENT_DELIVERY | TABLE | 14 | AR_STATEMENT_DELIVERY contains the information that is used for delivering customer statements via e... |
| AR_STATEMENT_HEADERS | TABLE | 54 | The AR_STATEMENT_HEADERS table is an interim table that Oracle Receivables uses when generating stat... |
| AR_STATEMENT_LINE_CLUSTERS | TABLE | 29 | The AR_STATEMENT_LINE_CLUSTERS table is an interim table that is used in statement generation and co... |
| AR_SUM_INCOMPLETE_TRX | TABLE | 7 | AR_SUM_INCOMPLETE_TRX is used in the Receivables Dashboard and displays the summary information of i... |
| AR_SUM_PENDING_CMAPP | TABLE | 7 | AR_SUM_PENDING_CMAPP is used in the Receivables Dashboard and displays the summary information for c... |
| AR_SUM_PENDING_RECAPP | TABLE | 8 | AR_SUM_PENDING_RECAPP is used in the Receivables Dashboard and displays the summary information of r... |
| AR_SUM_REF_EVENT_HIST | TABLE | 16 | The AR_SUM_REF_EVENT_HIST table temporarily stores the history of all AR business events that differ... |
| AR_TRANSACTION_HISTORY_ALL | TABLE | 32 | AR_TRANSACTION_HISTORY_ALL contains detailed information about each bills receivable transaction, in... |
| AR_TRANSMISSIONS_ALL | TABLE | 35 | The AR_TRANSMISSIONS_ALL table stores information about each Lockbox transmission. Each row includes... |
| AR_TRANSMISSION_FORMATS | TABLE | 16 | The AR_TRANSMISSION_FORMATS table contains information about the Lockbox transmission formats that y... |
| AR_TRANS_FIELD_FORMATS | TABLE | 22 | The AR_TRANS_FIELD_FORMATS table stores information about each field in a transmission format. You s... |
| AR_TRANS_RECORD_FORMATS | TABLE | 14 | The AR_TRANS_RECORD_FORMATS table stores information about each record in a transmission format, suc... |
| AR_TRX_BAL_SUMMARY | TABLE | 42 | This table stores the fields that summarize data over time, such as, Open Balance, Open Invoices Cou... |
| AR_TRX_DIST_LINE_BALANCES_ALL | TABLE | 27 | The AR_TRX_DIST_LINE_BALANCES_ALL table stores receivables data abstracted from standard receipts an... |
| AR_TRX_SUMMARY | TABLE | 51 | This table stores the fields, such as 'Total Invoices Value', 'Total Invoices Count', 'Total Cash Re... |
| AR_TRX_SUMMARY_HIST | TABLE | 23 | This table stores the history of all the modifications performed on different transactions, which wo... |
| AR_UPD_BANK_ACCOUNTS | TABLE | 32 | AR_UPD_BANK_ACCOUNTS contains customer bank account interface data entered into a simplified custome... |
| AR_UPD_BNKACCT_ERRORS | TABLE | 14 | AR_UPD_BNKACCT_ERRORS contains data validation error information for customer bank account interface... |
| AR_UPD_CONTACTS | TABLE | 96 | AR_UPD_CONTACTS contains customer contact interface data entered into a simplified customer spreadsh... |
| AR_UPD_CONTACTS_ERRORS | TABLE | 35 | AR_UPD_CONTACTS_ERRORS contains data validation error information for customer contact interface dat... |
| AR_UPD_CUSTOMERS | TABLE | 86 | AR_UPD_CUSTOMERS contains customer data entered into a simplified customer spreadsheet template for ... |
| AR_UPD_CUST_ERRORS | TABLE | 28 | AR_UPD_CUST_ERRORS contains data validation error information for customer interface data that faile... |
| AR_UPD_ERROR_DETAILS | TABLE | 11 | AR_UPD_ERROR_DETAILS contains mapping information between the staging table record and its error mes... |
| AR_UPD_REFACCT_ERRORS | TABLE | 15 | AR_UPD_REFACCT_ERRORS contains data validation error information for customer reference account inte... |
| AR_UPD_REF_ACCOUNTS | TABLE | 56 | AR_UPD_REF_ACCOUNTS contains customer reference account interface data entered into a simplified cus... |
| AR_XLA_LINES_EXTRACT | TABLE | 117 | AR_XLA_LINES_EXTRACT is a temporary table that contains the extracted accounting lines belonging to ... |
| CE_ACCT_HISTORY | TABLE | 22 | CE_ACCT_HISTORY contains information about account history. |
| CE_ACCT_TRX_CREAT_RULES | TABLE | 10 | CE_ACCT_TRX_CREAT_RULES contains information related to bank account transaction creation rules. |
| CE_AP_PM_DOC_CATEGORIES | TABLE | 10 | CE_AP_PM_DOC_CATEGORIES contains information about payment document categories and payment methods f... |
| CE_BALANCE_ACCT_GROUP | TABLE | 9 | This table contains the details of the bank account groups defined by users |
| CE_BANK_ACCOUNTS | TABLE | 94 | CE_BANK_ACCOUNTS contains Legal Entity Level bank account information. Each bank account must be aff... |
| CE_BANK_ACCOUNT_CASH_CCIDS | TABLE | 13 | This table stores the cash account flexfield identifiers for bank accounts that use multiple cash ac... |
| CE_BANK_ACCOUNT_GRANTS | TABLE | 14 | CE_BANK_ACCOUNT_GRANTS contains information about bank account grants. |
| CE_BANK_ACCT_USES_ALL | TABLE | 37 | CE_BANK_ACCT_USES_ALL contains Operating Unit level bank account use information. |
| CE_BANK_BRANCH_IDENTIFIERS | TABLE | 12 | This table stores the information about the network specific identifiers of banks or branches |
| CE_BAT_TRANSFERS | TABLE | 44 | This table contains the details of the bank account transfer and ad hoc payment transactions. |
| CE_CASH_POOLS | TABLE | 14 | This table stores the cash pools set up to aggregate bank account balances for the purpose of optimi... |
| CE_CASH_POOL_MEMBERS | TABLE | 11 | This table stores the subsidiary members that comprise a cash pool. A member can be bank account or ... |
| CE_CHECKBOOKS | TABLE | 13 | CE_CHECKBOOKS contains information related to payment checkbook. |
| CE_CONTACT_ASSIGNMENTS | TABLE | 12 | CE_CONTACT_ASSIGNMENTS contains the information about the level (bank, branch, account) to which the... |
| CE_CP_BANK_ACCOUNT_DIM | TABLE | 10 | This table contains the bank account dimension. |
| CE_CP_BANK_DIM | TABLE | 6 | This table contains the bank dimension. |
| CE_CP_CASH_POOL_DIM | TABLE | 10 | This table stores the entries for cash pool dimension that are maintained for cash position and fore... |
| CE_CP_CUBE_DIMENSIONS | TABLE | 10 | This table contains the custom cube dimensions defined by users. |
| CE_CP_CURRENCY_DIM | TABLE | 6 | This table contains the currency dimension. |
| CE_CP_CUSTOM_DIM | TABLE | 7 | This table contains the custom dimension. |
| CE_CP_DIMENSION_MAPPING | TABLE | 8 | This table stores the mapping of dimension member names that are greater than 80 characters or have ... |
| CE_CP_DIMENSION_SOURCES | TABLE | 13 | This table contains the source attributes that each dimension is mapped to. |
| CE_CP_DRILLTHROUGHS | TABLE | 7 | This table contains the application short name. |
| CE_CP_FACTS | TABLE | 92 | This table contains the fact data to build the cube. |
| CE_CP_GL_PERIODS_DIM | TABLE | 9 | This interface table contains the Fusion Financials GL periods dimension. |
| CE_CP_LAST_JOB_RUNS | TABLE | 7 | This table contains the job name and time that ran last time. |
| CE_CP_LEGAL_ENTITY_DIM | TABLE | 8 | This table contains the legal entity dimension. |
| CE_CP_LEGAL_ENTITY_REGION_DIM | TABLE | 6 | This table contains the legal entity region dimension. |
| CE_CP_OPTIONS | TABLE | 16 | This table contains the cash positioning and forecasting data extraction start date. |
| CE_CP_OPTION_TIME_DIMS | TABLE | 9 | This table contains the accounting calendar used to create the time dimension for the cash positioni... |
| CE_CP_SOURCE_DIM | TABLE | 6 | This table contains the source dimension. |
| CE_CP_SOURCE_SYSTEM_DIM | TABLE | 6 | This table contains the application dimension. |
| CE_CP_TRANSACTION_TYPES_DIM | TABLE | 6 | This table contains the transaction type dimension. |
| CE_CP_USER_ACCESS | TABLE | 8 | This table contains the user name with access to bank account. |
| CE_CTRY_SPECIFIC_UI_RULES | TABLE | 17 | This table contains the metadata country specific display rules for each country. |
| CE_EXTERNAL_TRANSACTIONS | TABLE | 32 | CE_EXTERNAL_TRANSACTIONS contains information related to external transactions. |
| CE_FINANCING_PROGRAMS_B | TABLE | 27 | This table contains information about financing program. |
| CE_FINANCING_PROGRAMS_TL | TABLE | 14 | This table is the translation table for CE_FINANCING_PROGRAMS_B. |
| CE_FIN_PROGRAM_CAMPAIGNS_B | TABLE | 21 | This table contains financing program campaign Information. |
| CE_FIN_PROGRAM_CAMPAIGNS_TL | TABLE | 11 | This table is the translation table for CE_FIN_PROGRAM_CAMPAIGNS_B. |
| CE_FIN_PROGRAM_CONTROLS | TABLE | 16 | This table contains program control information for financing programs. |
| CE_FIN_PROGRAM_LE_ASSOC | TABLE | 12 | This table contains the relationship between financial programs and associated legal entities. |
| CE_FIN_PROGRAM_OFFERS | TABLE | 27 | This table contains financing program offer information. |
| CE_GL_ACCOUNTS_CCID | TABLE | 25 | CE_GL_ACCOUNTS_CCID contains information about code combination identifiers per bank account use. |
| CE_INDEX_BANKS | TABLE | 17 | This table contains bank information. |
| CE_INDEX_BANK_BRANCHES | TABLE | 24 | This table contains bank branch information. |
| CE_INSTRUMENT_ATTRIBUTES | TABLE | 19 | This table stores the information about the additional attributes associated to an entity that are s... |
| CE_JE_MAPPINGS | TABLE | 21 | CE_JE_MAPPINGS contains the journal entry mappings information for a given bank account. Each row in... |
| CE_JE_MESSAGES | TABLE | 10 | CE_JE_MESSAGES contains the errors that occurred during the Journal Entry Creation program execution... |
| CE_PARSING_RULES | TABLE | 15 | CE_PARSING_RULES Contains information about parsing rules. |
| CE_PARSING_RULE_SETS | TABLE | 10 | CE_PARSING_RULE_SETS contains information about parsing rule sets. |
| CE_PAYEES | TABLE | 12 | This table contains payee information used for ad hoc payments. |
| CE_PAYMENT_DOCUMENTS | TABLE | 21 | CE_PAYMENT_DOCUMENTS contains information related to payment documents. |
| CE_PAYMENT_INSTRUMENTS | TABLE | 35 | This table stores the information of all the available payment instruments. |
| CE_PGM_THIRD_PARTY_CAND_HIST | TABLE | 20 | This table contains the change history for financing program candidates. |
| CE_PGM_THIRD_PTY_CANDIDATES | TABLE | 34 | This table contains information related to third parties that are candidates for financing programs. |
| CE_PGM_THIRD_PTY_ENROLLMENT | TABLE | 17 | ce_pgm_third_pty_enrollment stores information about third parties enrolled into various financing p... |
| CE_PGM_THIRD_PTY_LE_ASSOC | TABLE | 11 | This table contains the relationship between third parties enrolled into a financial program and app... |
| CE_PMT_INSTR_BU_ASSIGNMENTS | TABLE | 17 | This table stores the information about the operating units associated to a payment instrument |
| CE_RECON_EXCEPTIONS | TABLE | 15 | CE_RECON_EXCEPTIONS contains information about reconciliation exceptions. |
| CE_RECON_HISTORY | TABLE | 13 | CE_RECON_HISTORY contains information about reconciliation history. |
| CE_RECON_HISTORY_ITEMS | TABLE | 13 | CE_RECON_HISTORY_ITEMS contains information about reconciliation history items. |
| CE_RECON_MATCHING_RULES | TABLE | 27 | CE_RECON_MATCHING_RULES contains reconciliation matching rules that are used during automatic reconc... |
| CE_RECON_RULESETS | TABLE | 10 | CE_RECON_RULESETS contains the reconciliation rule sets. Reconciliation rule sets are used during au... |
| CE_RECON_RULESET_ITEMS | TABLE | 11 | CE_RECON_RULESET_ITEMS contains items that belong to reconciliation rule sets. |
| CE_RECON_RULE_GROUPBYS | TABLE | 10 | CE_RECON_RULE_GROUPBYS contains the attribute grouping information for one to many, many to one, or ... |
| CE_RECON_TOLERANCE_RULES | TABLE | 19 | CE_RECON_TOLERANCE_RULES contains tolerance rule definitions. Tolerance rules are used during reconc... |
| CE_STATEMENT_HEADERS | TABLE | 24 | CE_STATEMENT_HEADERS contains the statement header information. |
| CE_STATEMENT_LINES | TABLE | 51 | CE_STATEMENT_LINES contains information about statement lines. |
| CE_STMT_BALANCES | TABLE | 13 | CE_STMT_BALANCES contains information about statement balances. |
| CE_STMT_BAL_AVALBTY | TABLE | 12 | CE_STMT_BAL_AVALBTY contains information related to bank balance distributed availability. |
| CE_STMT_IMPORT_ERRORS | TABLE | 14 | CE_STMT_IMPORT_ERRORS contains information related to statement import errors. |
| CE_STMT_LINE_AVALBTY | TABLE | 11 | CE_STMT_LINE_AVALBTY contains information about statement line availability. |
| CE_STMT_LINE_CHARGES | TABLE | 17 | CE_STMT_LINE_CHARGES contains information about statement line charges. |
| CE_TRANSACTION_CODES | TABLE | 14 | CE_TRANSACTION_CODES contains information on transaction codes. |
| CE_TRX_TYPE_MAPPING | TABLE | 16 | CE_TRX_TYPE_MAPPING contains the transaction type for payment or receipt method mapping information. |
| EXM_ACCOM_POLICIES | TABLE | 28 | This table contains details of all accommodation policies. |
| EXM_ACCOM_POL_LINES | TABLE | 32 | This table contains details of a given accommodation policy. |
| EXM_ADDON_MILEAGE_RATES | TABLE | 11 | This table contains the additional rates for a mileage expense. |
| EXM_AIRFARE_POLICIES | TABLE | 19 | This table contains details of all airfare policies. |
| EXM_AIRFARE_POL_LINES | TABLE | 21 | This table contains details of a given airfare policy. |
| EXM_AUDIT_QUEUES | TABLE | 8 | This table contains the list of expense reports selected for audit and the assigned auditors. |
| EXM_AUDIT_REASONS | TABLE | 11 | This table contains the reasons for selecting an expense report for audit. |
| EXM_AUD_LIST_MEMBERS | TABLE | 13 | This table contains the list of individuals whose expense reports are always audited. |
| EXM_AUD_LIST_RULE_SETS | TABLE | 22 | This table contains the rules for including employees in expense audit list. |
| EXM_AUD_RULE_ASSIGNMENTS | TABLE | 12 | This table contains the assignment of a specific rule set, such as audit selection rule set, audit l... |
| EXM_AUD_RULE_SETS | TABLE | 62 | This table contains rule sets that identify the expense reports to be audited. For example, a rule s... |
| EXM_CARDS | TABLE | 27 | This table contains the corporate cards issued to individuals of the deploying company and the detai... |
| EXM_CARD_CURRENCIES | TABLE | 11 | This table contains the currencies used for corporate card transaction processing and the mapping be... |
| EXM_CARD_EMP_CANDIDATES | TABLE | 8 | This table contains the individuals identified as potential card holders for new corporate cards by ... |
| EXM_CARD_EXP_TYPE_MAPS | TABLE | 11 | This table contains the mapping between corporate card expense types and expense types in an expense... |
| EXM_CARD_HOLDER_DETAILS | TABLE | 15 | This table contains the details of the corporate card holders, such as name and employee number. |
| EXM_CARD_PROGRAMS | TABLE | 13 | This table contains the agreement between the corporate card issuer and the deploying company that g... |
| EXM_CARD_USAGE | TABLE | 12 | This table contains the detailed information about cards in scanned receipts for the expense payment... |
| EXM_CARRENTAL_POLICIES | TABLE | 25 | Table containing the car Rental Policy header records. |
| EXM_CARRENTAL_POL_LINES | TABLE | 27 | This table contains details of a given car rental policy. |
| EXM_CASH_ADVANCES | TABLE | 37 | This table contains the details of the travel advances issued to employees, such as cash advance num... |
| EXM_CASH_ADV_APPLICATIONS | TABLE | 20 | EXM_CASH_ADV_APPLICATIONS table stores detailed inoformation of cash advance applications. |
| EXM_CASH_ADV_HISTORY | TABLE | 16 | EXM_CASH_ADV_HISTORY table stores history of cash advances. |
| EXM_CATEGORY_FIELDS | TABLE | 21 | This table contains the data elements that needs to be captured for an expense category for a busine... |
| EXM_CC_ACCEPTORS | TABLE | 20 | This table contains the merchants who provide Level 3 detail transactions and the average time for p... |
| EXM_CC_AUTH_TRXNS | TABLE | 50 | This table contains corporate card transaction authorization data from corporate card issuers. |
| EXM_CC_COMPANY_ACCOUNTS | TABLE | 39 | This table contains the business units that are responsible for payment to the card issuer, payment ... |
| EXM_CC_DOWNLOAD_PARAMS | TABLE | 18 | This table contains the parameters used to automatically download corporate card transaction files f... |
| EXM_CC_OUTSTND_TRXN_SUM | TABLE | 17 | This table contains summarized aging information of outstanding corporate card transactions by compa... |
| EXM_CC_TRXN_DETAILS | TABLE | 15 | This table contains Level 3 details of corporate card transactions. |
| EXM_CC_TRXN_FILE_DETAILS | TABLE | 15 | This table contains the details of processed corporate card transaction files. |
| EXM_CC_UPLOAD_RULES | TABLE | 18 | This table contains the rules applied to a corporate card transaction file upload, such as employee ... |
| EXM_CONTING_WORK_SUPPL_MAP | TABLE | 15 | Table containing Contingent Worker Supplier Map records. |
| EXM_CREDIT_CARD_TRXNS | TABLE | 161 | This table contains the details of corporate card transactions and summary details as provided by th... |
| EXM_CUMUL_MILEAGE_DETERMINANTS | TABLE | 19 | This table contains elements that determine cumulative mileage for employees in a business unit and ... |
| EXM_DELEGATIONS | TABLE | 19 | This table contains the list of individuals and the persons they have authorized to enter expense re... |
| EXM_EMAIL_RECEIPT_IMPORT | TABLE | 27 | This table contains receipt details retrieved from an email server that were emailed by users to cre... |
| EXM_ENTERTAINMENT_POLICIES | TABLE | 47 | This table contains all data related to a given entertainment policy. |
| EXM_ENTERTAINMENT_POL_LINES | TABLE | 22 | This table contains the details of a given entertainment policy. Each line in the table contains an ... |
| EXM_EXCH_RATE_OPTIONS | TABLE | 13 | This table contains the conversion rate policies for business units. |
| EXM_EXCH_RATE_TOLERANCES | TABLE | 13 | This table contains the conversion rate policy exceptions for specific currencies within a business ... |
| EXM_EXPENSES | TABLE | 148 | EXM_EXPENSES stores detailed information about expense items for individual expense reports you ente... |
| EXM_EXPENSE_ATTENDEES | TABLE | 23 | This table contains the attendees for an entertainment expense. |
| EXM_EXPENSE_ATTENDEE_FAVS | TABLE | 19 | This table contains the attendee favorites for an entertainment expense. |
| EXM_EXPENSE_AUDIT_REASONS | TABLE | 11 | This table contains the reasons for selecting an expense item for audit. |
| EXM_EXPENSE_AUDIT_TRAILS | TABLE | 12 | This table contains a snapshot of the expense information for individual expenses within an expense ... |
| EXM_EXPENSE_DAILY_AMOUNTS | TABLE | 11 | This table contains the cumulative daily amounts for the expenses created by an employee on a specif... |
| EXM_EXPENSE_DISTS | TABLE | 113 | This table is used to store distribution information for a specific expense line. The table is a mul... |
| EXM_EXPENSE_ERRORS | TABLE | 56 | This table stores information about validations and policy violations that are used to create expens... |
| EXM_EXPENSE_PASSENGERS | TABLE | 12 | This table contains passenger expenses information for a mileage expense such as passenger name, dis... |
| EXM_EXPENSE_PERDIEM_DESTS | TABLE | 19 | This table contains expense per diem destinations. |
| EXM_EXPENSE_PERDIEM_DETAILS | TABLE | 29 | This table contains expense per diem details. |
| EXM_EXPENSE_PREDICTIONS | TABLE | 31 | EXM_EXPENSE_PREDICTIONS contains the predicted values from Intelligent Document Recognition and smar... |
| EXM_EXPENSE_REPORTS | TABLE | 56 | This table contains the general information for expense reports, such as the report number, purpose ... |
| EXM_EXPENSE_RISK_INDICATORS | TABLE | 20 | This table contains the information related to expense report risk. |
| EXM_EXPENSE_SPLIT_RATES | TABLE | 14 | This table contains the split rates for a mileage expense. |
| EXM_EXPENSE_TEMPLATES | TABLE | 25 | This table contains sets of expense types grouped for specific purposes by business unit, such as Ed... |
| EXM_EXPENSE_TOOLTIP_STATUSES | TABLE | 10 | This table contains details of tooltip statuses used in Expenses. |
| EXM_EXPENSE_TYPES | TABLE | 64 | This table contains the expense types defined for an expense report template and the associated corp... |
| EXM_EXPENSE_TYPE_ITEMIZE | TABLE | 8 | This table contains the expense types that are allowed in itemization for a specific expense type. |
| EXM_EXPENSE_TYPE_SYNONYMS | TABLE | 12 | This table contains unique expense types and their synonyms across all business units. |
| EXM_EXPENSE_VIOLATIONS | TABLE | 20 | This table contains information about expense violations. |
| EXM_EXP_ITEMIZATION_SUMMARY | TABLE | 15 | This table contains the expense itemization details that are used to generate summary information fo... |
| EXM_EXP_REP_PROCESSING | TABLE | 21 | This table is used to store processing status for an expense report. |
| EXM_EXP_TYPE_ENTERT_POL_MAP | TABLE | 12 | This table contains expense entertainment policy assignments to expense types. |
| EXM_EXP_TYPE_PASS_NAME_MAP | TABLE | 13 | Table containing the passenger name policy records. |
| EXM_EXP_TYPE_PREFER_MAP | TABLE | 14 | This table stores mappings between expense types and preferred entities, such as agencies and mercha... |
| EXM_EXP_TYPE_PREF_AGNCY_MAP | TABLE | 14 | This table stores mappings between expense types and preferred agencies. |
| EXM_EXP_TYPE_RULES | TABLE | 14 | This table contains rule sets based on expense templates and expense types that identify expense rep... |
| EXM_EXP_TYPE_RULE_SETS | TABLE | 10 | This table contains rules on expense templates and expense types that identify expense reports to be... |
| EXM_FAILED_ITINERARIES | TABLE | 18 | This table contains the itineraries that failed the import process and the resulting errors. |
| EXM_ITINERARY_RESERVATIONS | TABLE | 72 | This table contains information about travel itinerary bookings or reservations made, which includes... |
| EXM_ITINERARY_SCHEDULE | TABLE | 13 | This table contains information for the Travel Itinerary Import processes that run for all booking s... |
| EXM_LOCATIONS | TABLE | 21 | Store locations from HZ_GEOGRAPHIES table. |
| EXM_MAP_CODES | TABLE | 12 | This table contains the mapping between a charge type in corporate card transaction files and a corp... |
| EXM_MAP_TYPES_B | TABLE | 16 | This table contains corporate card expense type mapping rules that translates charge types in corpor... |
| EXM_MAP_TYPES_TL | TABLE | 13 | This table contains the language specific translation for corporate card expense type mapping rules. |
| EXM_MATCHING_HISTORY | TABLE | 96 | This table contains the expense status, starting from creation to automatic sweep. |
| EXM_MEALS_POLICIES | TABLE | 31 | This table contains details of all meals policies. |
| EXM_MEALS_POL_LINES | TABLE | 28 | This table contains the details of a given meals policy. Each line in the table contains a meals pol... |
| EXM_MERCHANTS | TABLE | 19 | This table contains information about merchants for employee expenses. |
| EXM_MILEAGE_POLICIES | TABLE | 46 | This table contains mileage expense policy definitions. |
| EXM_MILEAGE_POL_LINES | TABLE | 35 | This table contains mileage rates for mileage expense policies. |
| EXM_MILEAGE_WAYPOINTS | TABLE | 13 | This table contains information of mileage waypoints used in trips. |
| EXM_MISC_POLICIES | TABLE | 37 | This table contains all data related to a given miscellaneous policy. |
| EXM_MISC_POL_LINES | TABLE | 33 | This table contains the details of a given miscellaneous policy. Each line in the table contains a m... |
| EXM_MOBILE_DEVICE_REGISTRY | TABLE | 10 | This table contains device identifiers for mobile devices that have enabled receipt of corporate car... |
| EXM_MOBILE_EXPENSE_MATCHES | TABLE | 19 | This table contains expense items created from mobile devices and expense items created from corpora... |
| EXM_NONEMP_ATTENDEES | TABLE | 22 | This table contains the information of nonemployee attendees. |
| EXM_NOTES | TABLE | 13 | This table contains all note information, including note text and note type. |
| EXM_ORG_SETTINGS | TABLE | 9 | This table contains the default settings at the business unit level for attributes such as Conversio... |
| EXM_OTBI_STATS_BASE_SUMMARY | TABLE | 44 | This table contains base summary information for Expenses OTBI statistics reporting. |
| EXM_OTBI_STATS_SUMMARY | TABLE | 42 | This table contains summary information for Expenses OTBI statistics reporting. |
| EXM_PERDIEM_POLICIES | TABLE | 88 | This table contains information about per diem policies, including fixed rate rules and rates. |
| EXM_PERDIEM_POL_LINES | TABLE | 64 | This table contains per diem policy lines which are per diem policy rules or rates that are not fixe... |
| EXM_PERDIEM_POL_VALUES | TABLE | 19 | This table contains per diem policy lines which are per diem policy rules or rates that are not fixe... |
| EXM_PERSONAL_EXPENSE_TYPES | TABLE | 13 | This table contains the card expense types and merchant category codes that are categorized as perso... |
| EXM_PERSON_CUM_MILEAGE | TABLE | 20 | This table contains expenses usage information for a person such as cumulative distance traveled wit... |
| EXM_POL_EXP_TYPE_MAP | TABLE | 12 | This table contains expense policy assignments to expense types. |
| EXM_PREFERENCES | TABLE | 37 | This table contains the session preferences of expense entry users. |
| EXM_PROJECT_EXP_TYPE_MAPS | TABLE | 9 | This table contains the mapping between an expense type and a project expense type by project busine... |
| EXM_RCPT_NOTIF_RULE_SETS | TABLE | 29 | This table contains the rules that define the type of receipts that are required, when the individua... |
| EXM_RECENT_LOCATIONS | TABLE | 13 | This table contains information about recent locations to which an employee traveled. |
| EXM_RECURRING_SCHEDULES | TABLE | 10 | This table contains all recurring schedule information. |
| EXM_RESERVATION_ITEMS | TABLE | 49 | This table contains information about reservation items such as air or rail travel segments. |
| EXM_SETUP_OPTIONS | TABLE | 10 | This table contains the configuration for the entire installation, such as enabling the bar code in ... |
| EXM_SPEND_AUTHORIZATIONS | TABLE | 32 | This table contains the general information for spend authorizations, such as the authorization numb... |
| EXM_SPEND_AUTH_DISTS | TABLE | 47 | This table contains distribution information for a specific spend authorization expense line. |
| EXM_SPEND_AUTH_LINES | TABLE | 45 | This table contains detailed information about spend authorization lines entered by the individual. |
| EXM_SPEND_AUTH_PROCESSING | TABLE | 14 | This table contains the processing status for a spend authorization. |
| EXM_SPEND_AUTH_REPORT_MAP | TABLE | 10 | This table contains mappings between spend authorizations and expense reports. |
| EXM_SPLIT_ALLOCATIONS | TABLE | 80 | This table contains information about the split allocation of expense items among projects or busine... |
| EXM_SPLIT_ALLOCATION_SETS | TABLE | 14 | This table contains information about split allocation sets of expense items in expense reports. |
| EXM_SUBMISSION_LIMITS | TABLE | 12 | This table contains corporate card usage rules by business unit. An example of a rule is that employ... |
| EXM_TRAVEL_BOOKING_SITES | TABLE | 20 | This table contains detailed information of travel booking sites associated with each travel partner... |
| EXM_TRAVEL_DATA_ATTR_VAL_ERRS | TABLE | 11 | This table contains information about the itinerary, reservation or reservation item attribute valid... |
| EXM_TRAVEL_DATA_VAL_ERR_TYPES | TABLE | 20 | This table contains information about the validation error types that occurred for an itinerary, res... |
| EXM_TRAVEL_DATA_VAL_RULES | TABLE | 13 | This table contains information about validation rules to be applied to travel itineraries upon impo... |
| EXM_TRAVEL_INTEGRATIONS | TABLE | 17 | This table contains configuration information of travel partner integrations, such as single sign on... |
| EXM_TRAVEL_ITINERARIES | TABLE | 29 | This table contains summary information about imported travel itineraries from travel partners. |
| EXM_TRAVEL_SITE_COUNTRIES | TABLE | 11 | This table contains the countries assigned to or excluded from a travel booking site, depending on h... |
| EXM_TRAVEL_SITE_EMPLOYMENTS | TABLE | 13 | This table contains employment roles or job management levels assigned to or excluded from a travel ... |
| EXM_TRAVEL_VAL_RULE_SETS | TABLE | 11 | This table contains general information about sets of travel data validation rules that will be appl... |
| EXM_TRIPS | TABLE | 19 | This table contains general information about business trips associated with travel itineraries, cas... |
| EXM_USER_VENDOR_ENABLEMENT | TABLE | 11 | This table contains the enablement status of employees of a specific vendor. |
| EXM_VALIDATION_RESULTS | TABLE | 24 | This table contains validation results of spend authorization creation processes. |
| EXM_VAT_FIELDS | TABLE | 16 | This table contains tax data capture rules by territory for tax purposes. |
| EXM_VENDOR_ACCOUNTS | TABLE | 12 | This table contains the accounts representing the deploying company or its divisions that are regist... |
| EXM_VENDOR_ASSIGNMENTS | TABLE | 11 | This table contans the business units associated to the vendor accounts and status and selection cri... |
| EXM_VENDOR_EXPENSES | TABLE | 104 | The table stores expense data from various vendor integration points. |
| FA_ACE_BOOKS | TABLE | 19 | FA_ACE_BOOKS contains financial information for your Adjusted Current Earnings (ACE) depreciation bo... |
| FA_ADDITIONS_B | TABLE | 30 | FA_ADDITIONS_B contains descriptive information to help identify your assets. When adding an asset, ... |
| FA_ADDITIONS_TL | TABLE | 10 | FA_ADDITIONS_TL contains description translated in multiple language for the description columns in ... |
| FA_ADD_WARRANTIES | TABLE | 10 | FA_ADD_WARRANTIES contains information about the warranty that is attached to an asset. Oracle Fusio... |
| FA_ADJUSTMENTS | TABLE | 30 | FA_ADJUSTMENTS stores information that Oracle Assets needs to create journal entries for transaction... |
| FA_ADJUSTMENTS_T | TABLE | 256 | FA_ADJUSTMENTS_T is an interface table used for mass financial transactions. |
| FA_ADJ_SRC_LINES_T | TABLE | 75 | FA_ADJ_SRC_LINES_T contains mass source line adjustments. It is an interface table. Asset level info... |
| FA_APPROVAL_DETAILS | TABLE | 17 | This table stores the approval history details of each asset transaction that passes through the Ass... |
| FA_APPROVAL_SUMMARY | TABLE | 22 | This table stores the approval summary of each asset transaction that passes through the Asset Trans... |
| FA_ASSET_HISTORY | TABLE | 18 | FA_ASSET_HISTORY contains information about asset category change, capitalizations, unit adjustments... |
| FA_ASSET_INVOICES | TABLE | 71 | FA_ASSET_INVOICES contains the invoice information from Oracle Fusion Payables and Oracle Fusion Pur... |
| FA_ASSET_KEYWORDS | TABLE | 23 | FA_ASSET_KEYWORDS contains valid asset key flexfield segment value combinations. Segment values are ... |
| FA_ASSET_KEY_ALIASES_B | TABLE | 21 | FA_ASSET_KEY_ALIASES_B contains asset key aliases that represent frequently used category combinatio... |
| FA_ASSET_KEY_ALIASES_TL | TABLE | 12 | FA_ASSET_KEY_ALIASES_TL contains asset key alias names in installed languages. Each row includes the... |
| FA_BALANCES_EXTRACT | TABLE | 49 | This table contains data for asset balances subject area. |
| FA_BONUS_RATES | TABLE | 17 | FA_BONUS_RATES contains the bonus rates used by the depreciation program to calculate depreciation f... |
| FA_BONUS_RULES | TABLE | 22 | FA_BONUS_RULES contains information about your bonus depreciation rules. Oracle inserts a row into t... |
| FA_BOOKS | TABLE | 141 | FA_BOOKS contains the information needed for calculating depreciation. When you initially add an ass... |
| FA_BOOKS_SUMMARY | TABLE | 131 | FA_BOOKS_SUMMARY contains group assets periodical financial information. All group financial informa... |
| FA_BOOKS_SUMMARY_T | TABLE | 107 | This is a temporary table which is used internally by Oracle. |
| FA_BOOK_CONTROLS | TABLE | 145 | FA_BOOK_CONTROLS contains all information about the asset depreciation book. |
| FA_BOOK_CONTROLS_HISTORY | TABLE | 118 | FA_BOOK_CONTROLS_HISTORY contains information about modifications made to book setup information in ... |
| FA_BOOK_TRANSFERS_OPTIONS | TABLE | 38 | This table stores transfer transaction detail data of the source and destination asset book and tran... |
| FA_BOOK_TRANSFERS_POLICY | TABLE | 26 | This table stores transfer pricing rule data and other transfer rules required to transfer assets fr... |
| FA_BOOK_TRANSFER_DISTS | TABLE | 20 | This table contains asset distribution source and destination data for transfer between book transac... |
| FA_CALENDAR_PERIODS | TABLE | 12 | FA_CALENDAR_PERIODS contains detail information for FA_CALENDAR_TYPES. The depreciation program uses... |
| FA_CALENDAR_TYPES | TABLE | 13 | FA_CALENDAR_TYPES contains general information about depreciation calendars. Oracle Fusion Assets in... |
| FA_CASH_GEN_UNITS | TABLE | 11 | FA_CASH_GEN_UNITS contains the cash generating units defined for the asset books. |
| FA_CATEGORIES_B | TABLE | 29 | FA_CATEGORIES_B stores information about your asset categories. This table provides default informat... |
| FA_CATEGORIES_TL | TABLE | 10 | FA_CATEGORIES_TL contains translated description for columns in FA_CATEGORIES_B base table in multip... |
| FA_CATEGORY_ALIASES_B | TABLE | 21 | FA_CATEGORY_ALIASES_B contains asset category aliases that represent frequently used category combin... |
| FA_CATEGORY_ALIASES_TL | TABLE | 12 | FA_CATEGORY_ALIASES_TL contains asset category alias names in installed languages. Each row includes... |
| FA_CATEGORY_BOOKS | TABLE | 41 | FA_CATEGORY_BOOKS contains cost and reserve accounts for a book and category combination. A row inse... |
| FA_CATEGORY_BOOK_DEFAULTS | TABLE | 76 | FA_CATEGORY_BOOK_DEFAULTS contains the default depreciation rules that used for asset addition. A ro... |
| FA_CEILINGS | TABLE | 13 | FA_CEILINGS contains detail information about the depreciation expense, depreciation cost, and Inves... |
| FA_CEILING_TYPES | TABLE | 13 | FA_CEILING_TYPES contains the general information about the depreciation expense and cost ceilings. ... |
| FA_CONVENTIONS | TABLE | 10 | FA_CONVENTIONS contains detailed information about the prorate conventions. Oracle Fusion Assets use... |
| FA_CONVENTION_TYPES | TABLE | 13 | FA_CONVENTION_TYPES contains general information about the prorate conventions. The detail informati... |
| FA_DEFERRED_DEPRN | TABLE | 15 | FA_DEFERRED_DEPRN contains the deferred depreciation amounts calculated for each distribution of the... |
| FA_DEFERRED_DEPRN_EVENTS | TABLE | 12 | FA_DEFERRED_DEPRN_EVENTS contains information about the deferred depreciation events created by the ... |
| FA_DELETED_MASS_ADDITIONS | TABLE | 404 | FA_DELETED_MASS_ADDITIONS contains information about the mass additions that are deleted for audit t... |
| FA_DEPRN_BASIS_RULES | TABLE | 15 | FA_DEPRN_BASIS_RULES contains definitions of depreciable basis rules. Based on these definitions, Or... |
| FA_DEPRN_DETAIL | TABLE | 46 | FA_DEPRN_DETAIL contains the depreciation amounts that the depreciation program charges to the depre... |
| FA_DEPRN_DETAIL_H | TABLE | 48 | FA_DEPRN_DETAIL_H contains the depreciation information originally stored in FA_DEPRN_DETAIL for aud... |
| FA_DEPRN_EVENTS | TABLE | 14 | FA_DEPRN_EVENTS contains information about the events created during each depreciation run and if ap... |
| FA_DEPRN_EXTRACT | TABLE | 75 | FA_DEPRN_EXTRACT contains a denormalized and flattened representation of fixed assets and their depr... |
| FA_DEPRN_OVERRIDE | TABLE | 23 | FA_DEPRN_OVERRIDE contains depreciation information provided by users which overrides system calcula... |
| FA_DEPRN_PERIODS | TABLE | 16 | FA_DEPRN_PERIODS contains information about your depreciation periods. Oracle Fusion Assets uses thi... |
| FA_DEPRN_RULE_DETAILS | TABLE | 19 | This table defines detailed information for depreciable basis rule. It contains the available combin... |
| FA_DEPRN_SUMMARY | TABLE | 61 | FA_DEPRN_SUMMARY contains depreciation information for the assets. Each time the depreciation progra... |
| FA_DEPRN_SUMMARY_H | TABLE | 61 | FA_DEPRN_SUMMARY_H contains the depreciation information originally stored in FA_DEPRN_SUMMARY for a... |
| FA_DEPRN_TAX_AUTHORITIES | TABLE | 34 | FA_DEPRN_TAX_AUTHORITIES stores tax-authority-level information required by Japanese Depreciable Ass... |
| FA_DEPRN_TAX_NBVS_REP_T | TABLE | 21 | FA_DEPRN_TAX_NBVS_REP_T is used to track the previous reporting year's cost, the evaluated net book ... |
| FA_DEPRN_TAX_REP_T | TABLE | 37 | FA_DEPRN_TAX_REP_T is the Depreciable Assets Tax Reports interim table. |
| FA_DISTRIBUTION_DEFAULTS | TABLE | 12 | FA_DISTRIBUTION_DEFAULTS contains the distribution set default details for each distribution set. |
| FA_DISTRIBUTION_HISTORY | TABLE | 20 | FA_DISTRIBUTION_HISTORY contains information about the employee, location, and Accounting Flexfield ... |
| FA_DISTRIBUTION_SETS | TABLE | 12 | FA_DISTRIBUTION_SETS contains header information for each distribution set. |
| FA_FISCAL_YEAR | TABLE | 12 | FA_FISCAL_YEAR contains information about fiscal years. Oracle Fixed Assets uses this table to defin... |
| FA_FISCAL_YEAR_TYPES_B | TABLE | 8 | FA_FISCAL_YEAR_TYPES_B contains information about fiscal years. Oracle Fusion Assets uses this table... |
| FA_FISCAL_YEAR_TYPES_TL | TABLE | 10 | FA_FISCAL_YEAR_TYPES_TL contains information about fiscal years for translation. |
| FA_FLAT_RATES | TABLE | 15 | FA_FLAT_RATES contains the annual depreciation rates the depreciation program uses to calculate depr... |
| FA_FORMULAS | TABLE | 16 | FA_FORMULAS contains formulas used to calculate depreciation rates for formula-based methods. |
| FA_GROUP_REP_T | TABLE | 80 | This is a temporary table which is used internally by Oracle. |
| FA_IMPAIRMENTS | TABLE | 37 | FA_IMPAIRMENTS contains information about impairment transactions applied to assets or cash generati... |
| FA_INVENTORY | TABLE | 10 | This table stores audit trail information for the asset physical inventory. |
| FA_INVOICE_TRANSACTIONS | TABLE | 10 | FA_INVOICE_TRANSACTIONS tracks all the transactions you perform on invoice lines within Oracle Asset... |
| FA_ITC_RATES | TABLE | 12 | FA_ITC_RATES contains the rates for the investment tax credits. |
| FA_ITC_RECAPTURE_RATES | TABLE | 12 | FA_ITC_RECAPTURE_RATES contains the recapture rates for the investment tax credits. |
| FA_ITF_IMPAIRMENTS | TABLE | 104 | FA_ITF_IMPAIRMENTS contains information about impairment transactions. |
| FA_LEASES | TABLE | 39 | FA_LEASES contains information about lease assets including whether they are operating or capital le... |
| FA_LEASE_AMORT_SCHEDULES | TABLE | 51 | This table contains amortization schedules for each lease schedule. |
| FA_LEASE_BOOKS | TABLE | 58 | This table contains book level information of lease. |
| FA_LEASE_EXPENSE_DETAIL | TABLE | 31 | This table contains the lease interest expense and lease expense values for a leased asset for each ... |
| FA_LEASE_EXPENSE_DETAIL_H | TABLE | 30 | This table contains the lease expense and lease interest information originally stored in FA_LEASE_E... |
| FA_LEASE_EXPENSE_EVENTS | TABLE | 16 | This table contains information about the events created for lease expense and lease interest accoun... |
| FA_LEASE_EXPENSE_SUMMARY | TABLE | 34 | This table contains the lease interest expense and lease expense values for a leased asset for each ... |
| FA_LEASE_EXPENSE_SUMMARY_H | TABLE | 27 | This table contains the lease expense and lease interest information originally stored in FA_LEASE_E... |
| FA_LEASE_INVOICES | TABLE | 26 | This table contains the header details of each lease invoice. |
| FA_LEASE_INVOICE_LINES | TABLE | 15 | This table contains Invoces for each lease. |
| FA_LEASE_SCHEDULES | TABLE | 29 | This table contains lease schedule information of lease for lease and asset level. |
| FA_LEASE_SCHEDULE_ITEMS | TABLE | 31 | This table contains all the payment types and amounts for both lease and asset level schedule. |
| FA_LOCATIONS | TABLE | 21 | FA_LOCATIONS contains valid location flexfield segment value combinations. Oracle Fusion Assets uses... |
| FA_LOCATIONS_PRTL | TABLE | 3 | FA_LOCATIONS_PRTL contains valid location partial flexfield segment value combinations. This is just... |
| FA_LOCATION_ALIASES_B | TABLE | 21 | FA_LOCATION_ALIASES_B contains location aliases that represent frequently used category combinations... |
| FA_LOCATION_ALIASES_TL | TABLE | 12 | FA_LOCATION_ALIASES_TL contains asset location alias names in installed languages. Each row includes... |
| FA_LOCATION_MAPPINGS | TABLE | 13 | This table stores the location mapping between Assets and other models. |
| FA_MASSADD_DISTRIBUTIONS | TABLE | 51 | FA_MASSADD_DISTRIBUTIONS contains distribution information for each mass addition line. |
| FA_MASS_ADDITIONS | TABLE | 431 | FA_MASS_ADDITIONS stores information about assets that you want to automatically add to Oracle Asset... |
| FA_MASS_CHANGES | TABLE | 56 | This is an obsolete table and not in use. |
| FA_MASS_CHANGES_REP_T | TABLE | 36 | This is an obsolete table and not in use. |
| FA_MASS_RECLASS | TABLE | 94 | This is an obsolete table and not in use. |
| FA_MASS_RECLASS_REP_T | TABLE | 38 | This is an obsolete table and not in use. |
| FA_MASS_RETIREMENTS | TABLE | 102 | This is an obsolete table and not in use. |
| FA_MASS_RET_REP_T | TABLE | 20 | This is an obsolete table and not in use. |
| FA_MASS_REVAL_REP_T | TABLE | 32 | This is an obsolete table and not in use. |
| FA_MASS_TAX_ADJ_REP_T | TABLE | 18 | This is an obsolete table and not in use. |
| FA_MASS_TRANSACTIONS | TABLE | 145 | FA_MASS_TRANSACTIONS contains information about mass transaction requests. Oracle Fusion Assets stor... |
| FA_MASS_TRANSFERS | TABLE | 122 | This is an obsolete table and not in use. |
| FA_MASS_TRANSFERS_REP_T | TABLE | 12 | This is an obsolete table and not in use. |
| FA_MASS_TRX_DETAILS | TABLE | 124 | FA_MASS_TRX_DETAILS contains the new transaction details for mass transaction requests. Oracle Fusio... |
| FA_MC_ADJUSTMENTS | TABLE | 32 | FA_MC_ADJUSTMENTS contains information necessary for Oracle Fusion Assets to create journal entries ... |
| FA_MC_ASSET_INVOICES | TABLE | 71 | FA_MC_ASSET_INVOICES table contains accounts payable and purchasing information about assets in each... |
| FA_MC_BOOKS | TABLE | 145 | FA_MC_BOOKS contains currency and financial information about assets in each reporting book associat... |
| FA_MC_BOOKS_RATES | TABLE | 16 | FA_MC_BOOKS _RATES contains exchange rate information that Oracle Assets uses to convert transaction... |
| FA_MC_BOOKS_SUMMARY | TABLE | 132 | FA_MC_BOOKS_SUMMARY contains currency and financial information about asset depreciation in each rep... |
| FA_MC_BOOK_CONTROLS | TABLE | 26 | FA_MC_BOOK_CONTROLS table contains control information that affects all assets in a reporting deprec... |
| FA_MC_CONVERSION_HISTORY | TABLE | 17 | FA_MC_CONVERSION_HISTORY contains information about the conversion of asset transactions in a primar... |
| FA_MC_CONVERSION_RATES | TABLE | 16 | FA_MC_CONVERSION_RATES contains exchange rate information to convert assets from primary to reportin... |
| FA_MC_DEFERRED_DEPRN | TABLE | 16 | FA_MC_DEFERRED_DEPRN contains currency and financial information about deferred depreciation amounts... |
| FA_MC_DEPRN_DETAIL | TABLE | 57 | FA_MC_DEPRN_DETAIL contains currency and financial information about asset depreciation in each repo... |
| FA_MC_DEPRN_DETAIL_H | TABLE | 49 | FA_MC_DEPRN_DETAIL_H contains the depreciation information originally stored in FA_DEPRN_DETAIL for ... |
| FA_MC_DEPRN_PERIODS | TABLE | 17 | FA_MC_DEPRN_PERIODS contains information about your depreciation periods for each reporting book. It... |
| FA_MC_DEPRN_SUMMARY | TABLE | 61 | FA_MC_DEPRN_SUMMARY contains currency and financial information about asset depreciation in each rep... |
| FA_MC_DEPRN_SUMMARY_H | TABLE | 62 | FA_MC_DEPRN_SUMMARY_H contains the depreciation information originally stored in FA_MC_DEPRN_SUMMARY... |
| FA_MC_IMPAIRMENTS | TABLE | 38 | FA_MC_IMPAIRMENTS contains information about impairment transactions for each reporting book. |
| FA_MC_ITF_IMPAIRMENTS | TABLE | 103 | FA_MC_ITF_IMPAIRMENTS contains information about impairment transactions for each reporting book. |
| FA_MC_LEASE_AMORT_SCHEDULES | TABLE | 48 | This table contains amortization schedules for each lease schedule. |
| FA_MC_LEASE_BOOKS | TABLE | 59 | Table to store book level information for the lease. |
| FA_MC_LEASE_EXPENSE_DETAIL | TABLE | 32 | This table contains lease expense details for each asset associated to lease at distribution level. |
| FA_MC_LEASE_EXPENSE_DETAIL_H | TABLE | 32 | This table contains the history of lease expense and lease interest information for audit and inquir... |
| FA_MC_LEASE_EXPENSE_SUMMARY | TABLE | 33 | This table contains lease expense details for each asset associated to lease. |
| FA_MC_LEASE_EXPENSE_SUMMARY_H | TABLE | 33 | This table contains the history of lease expense and lease interest information for audit and inquir... |
| FA_MC_LEASE_SCHEDULES | TABLE | 32 | This table contains lease schedule information of lease for lease and asset level. |
| FA_MC_LEASE_SCHEDULE_ITEMS | TABLE | 32 | This table contains all the payment types and amounts for both lease and asset level schedule. |
| FA_MC_MASS_RATES | TABLE | 14 | FA_MC_MASS _RATES contains exchange rate information that Oracle Fusion Assets uses during the mass ... |
| FA_MC_RETIREMENTS | TABLE | 46 | FA_MC_RETIREMENTS contains currency and financial information about asset retirements in each report... |
| FA_MC_REVALUATIONS | TABLE | 48 | FA_MC_REVALUATIONS stores revaluation transaction related information at asset level in each reporti... |
| FA_METHODS | TABLE | 28 | FA_METHODS contains information on depreciation methods. The depreciation program uses this table to... |
| FA_PARALLEL_WORKERS | TABLE | 27 | This is a temporary table which is used internally by Oracle. |
| FA_PENDING_TRANSACTION_SUMMARY | TABLE | 11 | This table stores information of the count of pending financial transactions. |
| FA_PERIODIC_PRODUCTION | TABLE | 16 | FA_PERIODIC_PRODUCTION contains information on periodic production details for assets. |
| FA_PRICE_INDEXES | TABLE | 10 | FA_PRICE_INDEXES contains header level information of price index. |
| FA_PRICE_INDEX_VALUES | TABLE | 14 | FA_PRICE_INDEX_VALUE stores value of indexes for various period ranges in calendar for a price index... |
| FA_RATES | TABLE | 13 | FA_RATES stores the annual depreciation rates used by the depreciation program to calculate deprecia... |
| FA_RETIREMENTS | TABLE | 47 | FA_RETIREMENTS contains information about asset retirements. Oracle Fusion Assets inserts a row into... |
| FA_RETIREMENTS_T | TABLE | 132 | FA_RETIREMENTS_T contains temporary storage data for retirement transaction. |
| FA_RETIREMENT_DISTS_T | TABLE | 53 | FA_RETIREMENT_DISTS_T contains asset distribution details for unit retirements entered in the retire... |
| FA_RET_SRC_LINES_T | TABLE | 12 | FA_RET_SRC_LINES_T contains information of the source lines from retirement transactions. |
| FA_REVALUATIONS | TABLE | 54 | FA_REVALUATIONS stores revaluation transaction related information at asset level. |
| FA_SCHEDULE16_REP_T | TABLE | 67 | FA_SCHEDULE16_REP_T stores information required by Japanese Corporate Tax Schedule 16 Reports. |
| FA_SYSTEM_CONTROLS | TABLE | 16 | FA_SYSTEM_CONTROLS contains system-wide controls that affect all your assets. This table consists of... |
| FA_TRANSACTION_HEADERS | TABLE | 35 | Oracle Assets inserts rows to FA_TRANSACTION_HEADERS each time you enter a transaction. TRANSACTION_... |
| FA_TRANSFERS_T | TABLE | 63 | FA_TRANSFERS_T contains temporary storage data for asset transfer transactions. |
| FA_TRANSFER_DISTS_T | TABLE | 56 | FA_TRANSFERS_DISTS_T contains temporary storage data of asset distribution for transfer transactions... |
| FA_TRX_EXTRACT | TABLE | 64 | FA_TRX_EXTRACT contains a denormalized and flattened representation of fixed assets and their transa... |
| FA_TRX_REFERENCES | TABLE | 27 | FA_TRX_REFERENCES contains information about inter-asset transactions where two or more dependent tr... |
| FA_WARRANTIES | TABLE | 17 | FA_WARRANTIES contains information about asset warranties. |
| FA_WHATIF_REP_T | TABLE | 36 | This is a temporary table which is used internally by Oracle. |
| FA_WORK_ORDER_HEADERS | TABLE | 44 | FA_WORK_ORDER_HEADERS contains work orders that you want to add to assets. When adding a work order ... |
| FA_WORK_ORDER_LINES | TABLE | 83 | FA_WORK_ORDER_LINES contains work order line information for each work order. Each row represents a ... |
| FINANCIALS_SYSTEM_PARAMS_ALL | TABLE | 61 | FINANCIALS_SYSTEM_PARAMETERS_ALL contains options and defaults you share between your Oracle Payable... |
| FLA_ACCOUNTING_HEADERS_ALL | TABLE | 35 | FLA_ACCOUNTING_HEADERS_ALL contains accounting transactions generated within Lease Accounting for bo... |
| FLA_ACCOUNTING_LINES | TABLE | 37 | FLA_ACCOUNTING_LINES contains accounting transaction lines generated for FLA_ACCOUNTING_HEADERS_ALL. |
| FLA_ACCOUNTING_LINE_DETAILS | TABLE | 20 | FLA_ACCOUNTING_LINE_DETAILS contains accounting transaction lines details for FLA_ACCOUNTING_LINES |
| FLA_ACCOUNTING_TRANSACTIONS | TABLE | 21 | FLA_ACCOUNTING_TRANSACTIONS contains the transactions related to accounting. |
| FLA_ACCRUAL_SCHEDULES | TABLE | 48 | FLA_ACCRUAL_SCHEDULES contains period wise accural interest, amortization and lease expense. |
| FLA_ACCRUAL_SCHEDULES_STAGE | TABLE | 47 | fla_accrual_schedules_stage contains period wise accural interest, amortization and lease expense. |
| FLA_ASSET_IMPAIRMENTS | TABLE | 19 | FLA_ASSET_IMPAIRMENTS contains lease asset impairment details. |
| FLA_ASSET_IMPAIRMENTS_HIST | TABLE | 19 | FLA_ASSET_IMPAIRMENTS_HIST contains history of FLA_ASSET_IMPAIRMENTS. |
| FLA_ASSET_TEMPLATES_ALL | TABLE | 17 | FLA_ASSET_TEMPLATES_ALL contains setup of the asset template at the business unit level. |
| FLA_ASSET_TEMPLATE_ACCOUNTS | TABLE | 12 | FLA_ASSET_TEMPLATE_ACCOUNTS table is the detail table for FLA_ASSET_TEMPLATES_ALL and contains accou... |
| FLA_DISCOUNT_INDEXES_ALL | TABLE | 11 | FLA_DISCOUNT_INDEXES_ALL contains the cost of fund details such as name and start date . |
| FLA_DISCOUNT_INDEX_RATES_F | TABLE | 12 | FLA_DISCOUNT_INDEX_RATES_F is the lines table for FLA_DISCOUNT_INDEXES_ALL and stores the cost of fu... |
| FLA_INCREMENT_HEADERS | TABLE | 53 | FLA_INCREMENT_HEADERS contains the payment increase agreement details. |
| FLA_INCREMENT_HEADERS_HIST | TABLE | 54 | FLA_INCREMENT_HEADERS_HIST is the history table of FLA_INCREMENT_HEADERS |
| FLA_INCREMENT_INDEX_HDRS_ALL | TABLE | 14 | FLA_INCREMENT_INDEX_HDRS_ALL contains the payment increase index header details. |
| FLA_INCREMENT_INDEX_LINES | TABLE | 13 | FLA_INCREMENT_INDEX_LINES contains payment increase index line details. |
| FLA_INCREMENT_PAYMENTS | TABLE | 20 | FLA_INCREMENT_PAYMENTS contains payments which are part of the pay increase agreement |
| FLA_INCREMENT_PAYMENTS_HIST | TABLE | 20 | FLA_INCREMENT_PAYMENTS_HIST is the history table of FLA_INCREMENT_PAYMENTS. |
| FLA_INCREMENT_PERIODS | TABLE | 40 | FLA_INCREMENT_PERIODS contains payment increase assessment periods for the payment increase agreemen... |
| FLA_INCREMENT_PERIODS_HIST | TABLE | 40 | FLA_INCREMENT_PERIODS_HIST is the history table of FLA_INCREMENT_PERIODS. |
| FLA_INCREMENT_TEMPLATES_ALL | TABLE | 39 | FLA_INCREMENT_TEMPLATES_ALL contains the payment increase agreement templates. |
| FLA_LEASES_ALL | TABLE | 37 | FLA_LEASES_ALL contains lease information such as type of the lease, name of the lease, number, and ... |
| FLA_LEASE_ACTION_REQUESTS_ALL | TABLE | 77 | FLA_LEASE_ACTION_REQUESTS_ALL contains the actions requests for the lease, used for reporting purpos... |
| FLA_LEASE_ASSETS | TABLE | 71 | FLA_LEASE_ASSETS contains the asset details, which are part of the lease contract such as asset numb... |
| FLA_LEASE_ASSETS_HIST | TABLE | 71 | FLA_LEASE_ASSET_HIST contains the history of FLA_LEASE_ASSETS. |
| FLA_LEASE_ASSET_ACCOUNTS | TABLE | 20 | FLA_LEASE_ASSET_ACCOUNTS table has the account details for the accounting of asset level schedules. |
| FLA_LEASE_ASSET_ACCOUNTS_HIST | TABLE | 20 | FLA_LEASE_ASSET_ACCOUNTS_HIST table has the history information for the FLA_LEASE_ASSET_ACCOUNTS tab... |
| FLA_LEASE_ASSET_SERIALS | TABLE | 22 | FLA_LEASE_ASSET_SERIALS contains the asset serial details of the lease such as serial number and ins... |
| FLA_LEASE_ASSET_SERIALS_HIST | TABLE | 22 | FLA_LEASE_ASSET_SERIALS_HIST contains the history of FLA_LEASE_ASSET_SERIALS. |
| FLA_LEASE_BALANCES_ALL | TABLE | 40 | FLA_LEASE_BALANCES_ALL contains the scheduled and accounted balances for the leases. |
| FLA_LEASE_DETAILS | TABLE | 84 | FLA_LEASE_DETAILS table contains the lease version details like Lease End Date, Lease Classification... |
| FLA_LEASE_DETAILS_HIST | TABLE | 85 | FLA_LEASE_DETAILS_HIST contains the history of FLA_LEASE_DETAILS. |
| FLA_LEASE_ERRORS | TABLE | 23 | FLA_LEASE_ERRORS contains all the error messages which gets inserted while processing. |
| FLA_LEASE_INCREMENT_LINES | TABLE | 33 | FLA_LEASE_INCREMENT_LINES contains payment increase lines for the lease payment which is part of the... |
| FLA_LEASE_INCREMENT_LINES_HIST | TABLE | 33 | FLA_LEASE_INCREMENT_LINES_HIST is the history table of FLA_LEASE_INCREMENT_LINES. |
| FLA_LEASE_MILESTONES | TABLE | 28 | FLA_LEASE_MILESTONES contains lease milestones. |
| FLA_LEASE_OBLIGATIONS | TABLE | 31 | FLA_LEASE_OBLIGATIONS contains lease terms for obligations. |
| FLA_LEASE_OBLIGATIONS_HIST | TABLE | 31 | FLA_LEASE_OBLIGATIONS_HIST contains history of FLA_LEASE_OBLIGATIONS. |
| FLA_LEASE_PARTIES | TABLE | 17 | FLA_LEASE_PARTIES contains the Lease Parties which are part of the Lease Contract. This table retain... |
| FLA_LEASE_PARTIES_HIST | TABLE | 17 | FLA_LEASE_PARTIES_HIST contains the history of FLA_LEASE_PARTIES. |
| FLA_LEASE_PAYMENT_ACCOUNTS | TABLE | 21 | FLA_LEASE_PAYMENT_ACCOUNTS contains the payment account details for a lease payment header and retai... |
| FLA_LEASE_PAYMENT_ACCTS_HIST | TABLE | 21 | FLA_LEASE_PAYMENT_ACCTS_HIST contains the history of FLA_LEASE_PAYMENT_ACCOUNTS. |
| FLA_LEASE_PAYMENT_HDRS_HIST | TABLE | 137 | FLA_LEASE_PAYMENT_HDRS_HIST contains the history of FLA_LEASE_PAYMENT_HEADERS. |
| FLA_LEASE_PAYMENT_HEADERS | TABLE | 137 | FLA_LEASE_PAYMENT_HEADERS contains the payment details such as payment frequency, supplier informati... |
| FLA_LEASE_PAYMENT_LINES | TABLE | 34 | FLA_LEASE_PAYMENT_LINES contains the payment lines for a lease payment header and retains informatio... |
| FLA_LEASE_PAYMENT_LINES_HIST | TABLE | 34 | FLA_LEASE_PAYMENT_LINES_HIST contains the history of FLA_LEASE_PAYMENT_LINES. |
| FLA_LEASE_PAYMENT_TAXES | TABLE | 35 | FLA_LEASE_PAYMENT_TAXES contains the tax details of upfront tax rates and recovery tax rates for the... |
| FLA_LEASE_PAYMENT_TAXES_HIST | TABLE | 35 | FLA_LEASE_PAYMENT_TAXES_HIST contains the history of the FLA_LEASE_PAYMENT_TAXES table. |
| FLA_LEASE_POLICIES_ALL | TABLE | 13 | FLA_LEASE_POLICIES_ALL table has the policy information for the business unit which is applicable to... |
| FLA_LEASE_POLICY_LINES | TABLE | 21 | FLA_LEASE_POLICY_LINES table has the policy details for the lease policy. |
| FLA_LEASE_PRODUCTS_ALL | TABLE | 16 | FLA_LEASE_PRODUCTS_ALL table has the financial information for the lease like the lease accounting c... |
| FLA_LEASE_RIGHTS | TABLE | 24 | FLA_LEASE_RIGHTS contains lease terms for rights. |
| FLA_LEASE_RIGHTS_HIST | TABLE | 24 | FLA_LEASE_RIGHTS_HIST contains history of FLA_LEASE_RIGHTS. |
| FLA_LIABILITY_SCHEDULES | TABLE | 49 | FLA_LIABILITY_SCHEDULES contains cash , present value and liability schedules for the Schedules head... |
| FLA_LIABILITY_SCHEDULES_STAGE | TABLE | 48 | FLA_LIABILITY_SCHEDULES_STAGE is staging table created for FLA_LIABILITY_SCHEDULES. This will store ... |
| FLA_PAYMENT_ITEMS | TABLE | 120 | FLA_PAYMENT_ITEMS contains payment items data generated for the lease payments. |
| FLA_PAYMENT_TEMPLATES_ALL | TABLE | 53 | FLA_PAYMENT_TEMPLATES_ALL contains payment term template information such as supplier information, p... |
| FLA_PAYMENT_TEMPLATE_ACCOUNTS | TABLE | 13 | FLA_PAYMENT_TEMPLATE_ACCOUNTS table is the detail table for FLA_PAYMENT_TEMPLATES_ALL and contains a... |
| FLA_PAYMENT_TEMPLATE_TAXES | TABLE | 18 | FLA_PAYMENT_TEMPLATE_TAXES contains the tax details of upfront tax rates and recover tax rates for t... |
| FLA_PROPERTIES_ALL | TABLE | 29 | FLA_PROPERTIES_ALL contains property details. |
| FLA_PROPERTY_TYPES_ALL | TABLE | 10 | FLA_PROPERTY_TYPES_ALL contains property type setup details. |
| FLA_PROPERTY_TYPE_LEVELS | TABLE | 12 | FLA_PROPERTY_TYPE_LEVELS contains property type levels setup details. |
| FLA_SCHEDULE_HEADERS | TABLE | 121 | FLA_SCHEDULE_HEADERS contains schedule information at payment line and regime level for each transac... |
| FLA_SUBLEASE_ACTIVITY_DETAILS | TABLE | 20 | FLA_SUBLEASE_ACTIVITY_DETAILS contains the sublease activities with respect to its headlease. |
| FLA_SYSTEM_OPTIONS_ALL | TABLE | 62 | FLA_SYSTEM_OPTIONS_ALL contains setup options at the operating unit level. There is one row for each... |
| FLA_TAX_TRANSACTIONS | TABLE | 35 | FLA_TAX_TRANSACTIONS contains the tax transaction details for the payment. |
| FND_ACTIVITY_LOG | TABLE | 8 |  |
| FND_ACTIVITY_LOG_PARAMS | TABLE | 8 |  |
| FND_APM_BRANCHES | TABLE | 14 | This table stores APM Deploy branches information |
| FND_APM_BUILD | TABLE | 20 | This table contains apm build related objects. |
| FND_APM_BUILD_DEP_REPOS | TABLE | 17 | This table contains the list of dependent repositories for apm build objects. |
| FND_APM_META | TABLE | 12 |  |
| FND_APM_OBJECTS | TABLE | 12 | This table contains application objects. |
| FND_APPLCP_TEST | TABLE | 7 |  |
| FND_APPL_TAXONOMY | TABLE | 23 | Taxonomy table stores the various modules or artifacts that make up the Taxonomy hierarchy. |
| FND_APPL_TAXONOMY_ENT_APP_MAP | TABLE | 11 | New rdatabase table for EM equirement |
| FND_APPL_TAXONOMY_HIERARCHY | TABLE | 12 | Table for storing taxonomy module parent-child relationships. |
| FND_APPL_TAXONOMY_RF | TABLE | 13 | Taxonomy Row Flattening table required for Applcore Setup Admin UIs. |
| FND_APPL_TAXONOMY_TL | TABLE | 14 |  |
| FND_APPROVALS_BPM_PURGE | TABLE | 12 |  |
| FND_APPROVALS_INGEST_ERROR | TABLE | 11 | Stores task information for Approvals V2 ingestion for tasks that have errored and need to be retrie... |
| FND_APPROVALS_INGEST_STATUS | TABLE | 11 | Used to store the status and related metadata for the Approvals Ingestion jobs: Scheduler, Worker an... |
| FND_APPROVALS_PROXY_COMP_CFG | TABLE | 9 |  |
| FND_APPROVALS_PROXY_COMP_ROLES | TABLE | 9 |  |
| FND_APPROVALS_PROXY_USERS | TABLE | 19 |  |
| FND_APPROVALS_PROXY_USER_COMP | TABLE | 9 |  |
| FND_ATTACHED_DOCUMENTS | TABLE | 23 | The fnd attached documents table. |
| FND_ATTACHED_DOCUMENTS_TL | TABLE | 13 | Translation table for FND_ATTACHED_DOCUMENTS. This table is not currently used. |
| FND_AUDIT_ATTRIBUTES | TABLE | 20 | This table will store the attributes enabled for Auditing. |
| FND_AUDIT_BOSS_DEPLOYMENTS | TABLE | 14 | This table contains the deployed Business Object artifacts and related metadata for auditing. |
| FND_AUDIT_BOSS_USAGES | TABLE | 17 | This table contains the mapping between existing ADF and Business Objects |
| FND_AUDIT_CONFIG_METADATA | TABLE | 17 |  |
| FND_AUDIT_USER_TABLE_ACCESS | TABLE | 8 | This table stores the audit history on when a base table was last updated by a particular user. Ther... |
| FND_AUDIT_WEBAPP_AM | TABLE | 13 | This table contains seeded information on what AMs are available in a given webapp for Auditing. |
| FND_BOSS_AI_INVALID_INVK | TABLE | 6 | Invalid prompt invocation information collected during BOSS AI request |
| FND_BOSS_AI_LLM_INVK | TABLE | 4 | Successful prompt LLM invocation information used during a BOSS AI request |
| FND_BOSS_AI_TELEMETRY | TABLE | 12 | Used to store telemetry data related to a BOSS AI request. It contains request information along wit... |
| FND_BOSS_APPLICATION_CONFIG | TABLE | 8 | BOSS fnd_boss_application_config stores application config needed for boss application. |
| FND_BOSS_CLST_CLUSTERS | TABLE | 14 | Table used to store individual cluster information as the result of the execution of a clusterizatio... |
| FND_BOSS_CLST_ERIZATIONS | TABLE | 17 | Table that contain the main information needed to execute a clusterization process. |
| FND_BOSS_CLST_FEATURES | TABLE | 7 | Used to contain BOSS data clustering features referenced by fnd_boss_clusterization |
| FND_BOSS_CLST_JOBS | TABLE | 14 | Table that represents a clustering job associated to a clusterization process. |
| FND_BOSS_CLST_JOB_ERRORS | TABLE | 7 | Used to store error messages generated during a clustering job execution |
| FND_BOSS_DEPID_VECTOR_STATUS | TABLE | 8 |  |
| FND_BOSS_DEPLOYMENTS | TABLE | 8 |  |
| FND_BOSS_DEPLOYMENT_CACHE | TABLE | 12 |  |
| FND_BOSS_EMBEDDING_MODELS | TABLE | 8 |  |
| FND_BOSS_EXMPL_TO_QSTN | TABLE | 5 | Table used to relate LLM examples in fnd_boss_llm_examples to natural language questions in fnd_boss... |
| FND_BOSS_HS_BV_TO_INDEX | TABLE | 8 | Reference of BOSS RODS indexes to FND_BOSS_HV_INDICES. |
| FND_BOSS_HS_FUSION_INDICES | TABLE | 11 | BOSS RODS Hybrid Search indexes defined by BOSS metadata. |
| FND_BOSS_HS_INDEX_DATA | TABLE | 18 | BOSS RODS index physical storage information for indexes defined in FND_BOSS_HS_INDICES. |
| FND_BOSS_HS_INDICES | TABLE | 18 | BOSS RODS Hybrid Search indexes state defined by BOSS metadata. |
| FND_BOSS_LLM_EXAMPLES | TABLE | 9 | Table that contains information for ingested LLM example from metadata files. |
| FND_BOSS_LLM_QUESTIONS | TABLE | 6 | Table used to store natural language questions that will be used to match against an LLM example |
| FND_BOSS_PN_FUSION_METADATA | TABLE | 10 | BOSS proper name index physical storage information for indexes defined in FND_BOSS_PN_FUSION_METADA... |
| FND_BOSS_PN_METADATA | TABLE | 8 |  |
| FND_BOSS_SEARCH_BAD_RECORDS | TABLE | 12 | A dead record bin for data we cannot index, including reasons why. |
| FND_BOSS_SEARCH_DATA_CHUNK | TABLE | 19 | BOSS Search indexes defined by BOSS metadata. |
| FND_BOSS_SEARCH_INDEX_DATA | TABLE | 14 | BOSS Search indexes defined by BOSS metadata. |
| FND_BOSS_SEARCH_INDEX_FIELDS | TABLE | 11 | All fields defined in a BOSS Search index. |
| FND_BOSS_SEARCH_INDEX_TO_REF | TABLE | 9 | Record of the Reference Objects within the current Index. |
| FND_BOSS_SEARCH_INDEX_VIEWS | TABLE | 7 | BOSS Views used to derive Search indexes. |
| FND_BOSS_SEARCH_INDICES | TABLE | 19 | BOSS Search indexes defined by BOSS metadata. |
| FND_BOSS_TELEMETRY_LLM | TABLE | 2 |  |
| FND_BOSS_TEST_RESULTS | TABLE | 7 | Results of BOSS tests |
| FND_BOSS_TEST_STATUS | TABLE | 7 | Status of BOSS tests |
| FND_BPM_FACTS_B | TABLE | 18 |  |
| FND_BPM_FACTS_TL | TABLE | 13 |  |
| FND_BPM_FACT_JOINS | TABLE | 16 |  |
| FND_BPM_TASK_ASSIGNEE | TABLE | 14 |  |
| FND_BPM_TASK_ATTACHMENT | TABLE | 20 |  |
| FND_BPM_TASK_ATTRIBUTES_B | TABLE | 59 |  |
| FND_BPM_TASK_ATTRIBUTES_TL | TABLE | 14 |  |
| FND_BPM_TASK_ATTR_PROPS | TABLE | 15 |  |
| FND_BPM_TASK_B | TABLE | 29 |  |
| FND_BPM_TASK_COMMENT | TABLE | 14 |  |
| FND_BPM_TASK_COMPOSITES_B | TABLE | 33 |  |
| FND_BPM_TASK_COMPOSITES_TL | TABLE | 15 |  |
| FND_BPM_TASK_HISTORY_B | TABLE | 29 |  |
| FND_BPM_TASK_HISTORY_TL | TABLE | 14 |  |
| FND_BPM_TASK_TL | TABLE | 13 |  |
| FND_BULK_MERGE_ARCHIVE | TABLE | 6 |  |
| FND_BULK_MERGE_ERRORS | TABLE | 6 |  |
| FND_BULK_SEED_EXECUTIONS | TABLE | 6 |  |
| FND_BULK_SEED_EXECUTIONS_BK | TABLE | 6 |  |
| FND_CAL_DAY | TABLE | 15 | Day Level Table for Gregorian Calendar Time Dimension |
| FND_CAL_MONTH | TABLE | 16 | Month Level Table for Gregorian Calendar Time Dimension |
| FND_CAL_QUARTER | TABLE | 16 | Quarter Level Table for Gregorian Calendar Time Dimension |
| FND_CAL_WEEK | TABLE | 16 | Week Level Table for Gregorian Calendar Time Dimension |
| FND_CAL_YEAR | TABLE | 14 | Year Level Table for Gregorian Calendar Time Dimension |
| FND_CA_DEVICE_DIM | TABLE | 15 | This table provide visibility into our users devices and clients, such as device type, browser type,... |
| FND_CA_DEVICE_FACT | TABLE | 12 | The device metrics provide visibility into our users devices and clients, such as device type, brows... |
| FND_CA_ENGAGEMENT_FACT | TABLE | 20 |  |
| FND_CA_ENVIRONMENT_DIM | TABLE | 8 |  |
| FND_CA_FAMILY_DIM | TABLE | 7 |  |
| FND_CA_FAMILY_DIM_TL | TABLE | 9 | This table holds translatable information for Families |
| FND_CA_METRICS_BOOKKEEPING | TABLE | 14 |  |
| FND_CA_PAGE_DIM | TABLE | 10 |  |
| FND_CA_PAGE_DIM_TL | TABLE | 9 | This table holds translatable information for Pages |
| FND_CA_PAGE_GROUPING_DIM | TABLE | 13 |  |
| FND_CA_PRODUCT_DIM | TABLE | 8 |  |
| FND_CA_PRODUCT_DIM_TL | TABLE | 9 | This table holds translatable information for Products |
| FND_CA_SOURCE_ENTRY_DIM | TABLE | 7 |  |
| FND_CA_SOURCE_ENTRY_FACT | TABLE | 13 |  |
| FND_CA_TIMELINE_DIM | TABLE | 9 |  |
| FND_COLUMN_DATASHAPES | TABLE | 23 | This table will be used to maintain the Column level Datashape Info for all Fusion Tables and Column... |
| FND_COMPILED_MENU_FUNCTIONS | TABLE | 6 | compiled menu functions stores the compilation of menus/functions |
| FND_CONSOLE_ISSUE | TABLE | 39 |  |
| FND_CONSOLE_TRANSACTION_INFO | TABLE | 38 |  |
| FND_CSM_TBL_BACKUP | TABLE | 13 | This table is used to determine the backup table for each base table used for CSM import. This table... |
| FND_CURRENCIES_B | TABLE | 25 | FND_CURRENCIES_B |
| FND_CURRENCIES_TL | TABLE | 14 | FND_CURRENCIES_TL |
| FND_CURRENT_PILLAR_DATABASE | TABLE | 1 |  |
| FND_DBRM_DETAILS | TABLE | 15 |  |
| FND_DEEP_LINK_LIST | TABLE | 23 | This table contains the list of Deep Links created. Most of the deep links in the table are seeded. ... |
| FND_DEEP_LINK_LIST_BK | TABLE | 21 |  |
| FND_DEEP_LINK_LIST_PARAMS | TABLE | 15 |  |
| FND_DEEP_LINK_LIST_PARAMS_BK | TABLE | 16 |  |
| FND_DEPENDENCY_SET_B | TABLE | 8 |  |
| FND_DEPENDENCY_SET_TL | TABLE | 11 |  |
| FND_DF_ADFBC_USAGES | TABLE | 26 | Contains product delivered ADFBC metadata. |
| FND_DF_ADFBC_USAGES_BK | TABLE | 24 | Contains product delivered ADFBC metadata. |
| FND_DF_BOSS_USAGES | TABLE | 15 | This table stores the descriptive flexfield BOSS business object usages. |
| FND_DF_CONTEXTS_B | TABLE | 25 | Flexfields: Descriptive Flexfields: Context (_B) table. |
| FND_DF_CONTEXTS_B_BK | TABLE | 23 | Flexfields: Descriptive Flexfields: Context (_B) table. |
| FND_DF_CONTEXTS_TL | TABLE | 18 |  |
| FND_DF_CONTEXTS_TL_BK | TABLE | 16 |  |
| FND_DF_CTX_VALIDATORS_B | TABLE | 15 | Flexfields: Descriptive Flexfields: Context Validator (_B) table. |
| FND_DF_CTX_VALIDATORS_B_BK | TABLE | 13 | Flexfields: Descriptive Flexfields: Context Validator (_B) table. |
| FND_DF_CTX_VALIDATORS_TL | TABLE | 18 |  |
| FND_DF_CTX_VALIDATORS_TL_BK | TABLE | 16 |  |
| FND_DF_FLEXFIELDS_B | TABLE | 33 | Flexfields: Descriptive Flexfields: Descriptive Flexfield Registration (_B) Table |
| FND_DF_FLEXFIELDS_B_BK | TABLE | 31 | Flexfields: Descriptive Flexfields: Descriptive Flexfield Registration (_B) Table |
| FND_DF_FLEXFIELDS_SB | TABLE | 8 |  |
| FND_DF_FLEXFIELDS_TL | TABLE | 16 |  |
| FND_DF_FLEXFIELDS_TL_BK | TABLE | 14 |  |
| FND_DF_FLEX_USAGES_B | TABLE | 16 | Flexfields: Descriptive Flexfields: Flexfield Usage (_B) table. |
| FND_DF_FLEX_USAGES_B_BK | TABLE | 14 | Flexfields: Descriptive Flexfields: Flexfield Usage (_B) table. |
| FND_DF_FLEX_USAGES_TL | TABLE | 17 |  |
| FND_DF_FLEX_USAGES_TL_BK | TABLE | 15 |  |
| FND_DF_PARAMETERS | TABLE | 16 | Flexfields: Descriptive Flexfields: Parameters table. |
| FND_DF_PARAMETERS_BK | TABLE | 14 | Flexfields: Descriptive Flexfields: Parameters table. |
| FND_DF_SEGMENTS_B | TABLE | 45 | Flexfields: Descriptive Flexfields: Segment (_B) table. |
| FND_DF_SEGMENTS_B_BK | TABLE | 43 | Flexfields: Descriptive Flexfields: Segment (_B) table. |
| FND_DF_SEGMENTS_TL | TABLE | 23 |  |
| FND_DF_SEGMENTS_TL_BK | TABLE | 21 |  |
| FND_DF_SEGMENT_LABELS_B | TABLE | 14 |  |
| FND_DF_SEGMENT_LABELS_B_BK | TABLE | 12 |  |
| FND_DF_SEGMENT_LABELS_TL | TABLE | 17 |  |
| FND_DF_SEGMENT_LABELS_TL_BK | TABLE | 15 |  |
| FND_DF_TABLE_USAGES | TABLE | 19 | Flexfields: Descriptive Flexfields: Table Usages table. |
| FND_DF_TABLE_USAGES_BK | TABLE | 17 | Flexfields: Descriptive Flexfields: Table Usages table. |
| FND_DIAG_EXECUTION | TABLE | 14 | Stores information on every invocation of a test. |
| FND_DIAG_INPUTSET | TABLE | 13 | Stores input parameters so that a user can launch the same diagnostic run and reuse the inputs used ... |
| FND_DIAG_INPUTSET_NAME_VALUE | TABLE | 12 | Stores inputset name - value pairs for reusing the inputset in a later run of the same diagnostics. |
| FND_DIAG_INPUTSET_TL | TABLE | 14 | This table stores translatable attributes such as display name and description for diagnostic test i... |
| FND_DIAG_RUN | TABLE | 14 | Stores information on a Diagnostics test run. A Diagnostic run can be launched for any "taxonomy nod... |
| FND_DIAG_TAG | TABLE | 12 | This table defines tags, used to categorize diagnostic tests in a flexible fashion. TAGs are Module ... |
| FND_DIAG_TAG_TL | TABLE | 14 | Translations table for Tags (Flexible test categories) |
| FND_DIAG_TAG_VALUE | TABLE | 13 | This table defines Tag Value ID's, which is equivalent to Taxonomy's Module ID. |
| FND_DIAG_TAG_VALUE_HIERARCHY | TABLE | 11 | This table stores tag value id hierarchy data |
| FND_DIAG_TAG_VALUE_PREREQ | TABLE | 13 | Defines prerequisites for tag values. A tag value may declare other tag values as prequisites. |
| FND_DIAG_TAG_VALUE_TEST_ASSOC | TABLE | 13 | This table stores assignments of diagnostics tests to various tag value id's (TAG_VALUE_ID's represe... |
| FND_DIAG_TAG_VALUE_TL | TABLE | 14 | Translations for Tag Value table. |
| FND_DIAG_TEST | TABLE | 18 | Diagnosctic Tests registered |
| FND_DIAG_TEST_PARAM | TABLE | 13 | Parameters for Diagnostics Tests |
| FND_DIAG_TEST_PARAM_TL | TABLE | 16 | Translations for Input/output parameter definitions. |
| FND_DIAG_TEST_PREREQ | TABLE | 14 | Defines prerequisites for diagnostic tests. |
| FND_DIAG_TEST_STATS | TABLE | 17 | Captures statistics related to each diagnostic test execution. |
| FND_DIAG_TEST_TL | TABLE | 15 | Translations for Diagnostic Test definitions. |
| FND_DOCUMENTS | TABLE | 21 | This table stores the information about documents stored in the document repository. |
| FND_DOCUMENTS_TL | TABLE | 36 | This table contains the columns that require translation. |
| FND_DOCUMENT_CATEGORIES | TABLE | 13 | This is the document categories table and is used by attachments as a lookup for document categories... |
| FND_DOCUMENT_CATEGORIES_BK | TABLE | 11 | This is the document categories table and is used by attachments as a lookup for document categories... |
| FND_DOCUMENT_CATEGORIES_TL | TABLE | 14 | This table holds the translatable columns for document categories. |
| FND_DOCUMENT_CATEGORIES_TL_BK | TABLE | 12 | This table holds the translatable columns for document categories. |
| FND_DOCUMENT_ENTITIES | TABLE | 26 | The fnd_document_entities table contains data on the entities used within attachments. |
| FND_DOCUMENT_ENTITIES_BK | TABLE | 22 | The FND_DOCUMENT_ENTITIES_BK table contains data on the entities used within attachments. |
| FND_DOCUMENT_ENTITIES_TL | TABLE | 13 | This table contains the columns that require translation. |
| FND_DOCUMENT_ENTITIES_TL_BK | TABLE | 11 | This table contains the columns that require translation. |
| FND_DOCUMENT_FILE_FORMAT | TABLE | 12 | The table for tracking file formats of interest to Attachments. |
| FND_DOCUMENT_FILE_FORMAT_BK | TABLE | 10 | The table for tracking file formats of interest to Attachments. |
| FND_DOCUMENT_FILE_FORMAT_TL | TABLE | 14 | This table holds the translatable columns for document file formats. |
| FND_DOCUMENT_FILE_FORMAT_TL_BK | TABLE | 12 | This table holds the translatable columns for document file formats. |
| FND_DOCUMENT_SEQUENCES | TABLE | 24 |  |
| FND_DOC_CATEGORIES_TO_ENTITIES | TABLE | 12 | This table contains the attachment categories that are available for when working with an attachment... |
| FND_DOC_CATG_TO_ENTITIES_BK | TABLE | 10 | This table contains the backed up details of the FND_DOC_CATEGORIES_TO_ENTITIES table. |
| FND_DOC_LAWS_B | TABLE | 12 | Specifies a set of laws. These laws are applied to the attachments which are in scope. When a law is... |
| FND_DOC_LAWS_B_BK | TABLE | 10 | Specifies a set of laws. These laws are applied to the attachments which are in scope. When a law is... |
| FND_DOC_LAWS_TL | TABLE | 16 | Specifies a set of laws. These laws are applied to the attachments which are in scope. When a law is... |
| FND_DOC_LAWS_TL_BK | TABLE | 14 | Specifies a set of laws. These laws are applied to the attachments which are in scope. When a law is... |
| FND_DOC_POST_RENDITIONS | TABLE | 14 | New table tracking any artefacts that have been generated by the post processing that access could b... |
| FND_DOC_RULES | TABLE | 21 | Specifies the scopes and laws used to validate an attachments record before saving. |
| FND_DOC_RULES_BK | TABLE | 19 | Specifies the scopes and laws used to validate an attachments record before saving. |
| FND_DOC_SCOPES_B | TABLE | 14 | Specifies a set of scope rules. From this, it's possible to determine whether an attachment is in sc... |
| FND_DOC_SCOPES_B_BK | TABLE | 12 | Specifies a set of scope rules. From this, it's possible to determine whether an attachment is in sc... |
| FND_DOC_SCOPES_TL | TABLE | 14 | Specifies a set of scope rules. From this, it's possible to determine whether an attachment is in sc... |
| FND_DOC_SCOPES_TL_BK | TABLE | 12 | Specifies a set of scope rules. From this, it's possible to determine whether an attachment is in sc... |
| FND_DOC_SCOPE_TO_LAW_B | TABLE | 14 | Records the scope to rule mappings used to validate attachments. |
| FND_DOC_SCOPE_TO_LAW_B_BK | TABLE | 12 | Records the scope to rule mappings used to validate attachments. |
| FND_DOC_SCOPE_TO_LAW_TL | TABLE | 14 | Records the scope to rule mappings used to validate attachments. |
| FND_DOC_SCOPE_TO_LAW_TL_BK | TABLE | 12 | Records the scope to rule mappings used to validate attachments. |
| FND_DOC_SEQUENCE_ASSIGNMENTS | TABLE | 17 | FND_DOC_SEQUENCE_ASSIGNMENTS defines the relationship between the doc sequences and the related obje... |
| FND_DOC_SEQUENCE_AUDIT | TABLE | 9 | FND Document Sequence Audit Table |
| FND_DOC_SEQUENCE_CATEGORIES | TABLE | 15 | Document Sequential Numbering Categories |
| FND_DOC_SEQUENCE_USERS | TABLE | 11 |  |
| FND_DUAL | TABLE | 1 |  |
| FND_EDP_PROT_FIELDS_B | TABLE | 13 | Stores the definitions of the fields which are to be protected by an external application. |
| FND_EDP_PROT_FIELDS_TL | TABLE | 10 | Stores the translations for the definitions of the fields which are to be protected by an external a... |
| FND_EF_CATEGORIES_B | TABLE | 19 | The FND_EF_CATEGORIES_B table stores Category definitions for Extensible Flexfields. |
| FND_EF_CATEGORIES_B_BK | TABLE | 17 | The FND_EF_CATEGORIES_B_BK table stores Category definitions for Extensible Flexfields. |
| FND_EF_CATEGORIES_TL | TABLE | 15 | Translation table for Category definitions |
| FND_EF_CATEGORIES_TL_BK | TABLE | 13 | Translation table for Category definitions |
| FND_EF_CATEGORY_CONTEXTS | TABLE | 14 |  |
| FND_EF_CATEGORY_CONTEXTS_BK | TABLE | 12 |  |
| FND_EF_CONTEXT_USAGES | TABLE | 22 |  |
| FND_EF_CONTEXT_USAGES_BK | TABLE | 20 |  |
| FND_EF_UI_PAGES_B | TABLE | 19 |  |
| FND_EF_UI_PAGES_B_BK | TABLE | 17 |  |
| FND_EF_UI_PAGES_TL | TABLE | 20 |  |
| FND_EF_UI_PAGES_TL_BK | TABLE | 18 |  |
| FND_EF_UI_PAGE_TASK_FLOWS | TABLE | 20 | Extensible flexfield UI page context inclusions |
| FND_EF_UI_PAGE_TASK_FLOWS_BK | TABLE | 18 | Extensible flexfield UI page context inclusions |
| FND_ENT_APP_LIB_USAGE_MAP | TABLE | 8 |  |
| FND_ES_BPM_TASKS | TABLE | 5 |  |
| FND_EVB_DICTIONARY_ATTR_USAGE | TABLE | 7 | This table stores the dictionary attributes that are actually used in in the rule conditions and act... |
| FND_EVB_DICTIONARY_FACT | TABLE | 8 | This table stores the dictionary facts. These facts are used in the web service to execute the rules... |
| FND_EVB_DICTIONARY_ID | TABLE | 11 | This table stores the dictionary primary identifiers. These primary identifiers are used in the web ... |
| FND_EVB_DICTIONARY_LINKS | TABLE | 7 | This table stores the information about the linked dictionaries of one dictionary . These linked dic... |
| FND_EXTMGR_OBJECTS | TABLE | 8 | This table contains extension objects. |
| FND_EXTM_APP_REPO | TABLE | 13 | Extension Management APP Repo |
| FND_EXTM_BUILD | TABLE | 15 | Extension Management Request Status processing Information Table |
| FND_EXTM_EXTENSION_STATUS | TABLE | 26 | Extension Management Request Status processing Information Table |
| FND_FAVORITE_ITEMS | TABLE | 31 | This table is created to store favorite items created by logged in user in fusion applications. |
| FND_FA_IDCS_NOTIF_JOB_STATUS | TABLE | 37 | Version 2 of SaaS-PaaS sync job used for notifying the IDCS to sync users/roles and Role association... |
| FND_FF_COLUMN_USAGES | TABLE | 15 | Flexfields: Column Usages table |
| FND_FF_COLUMN_USAGES_BK | TABLE | 13 | Flexfields: Column Usages table |
| FND_FILE_UPLOAD_CHUNKS | TABLE | 13 | This table tracks the state of file chunks being uploaded for Attachments using a chunked background... |
| FND_FILE_UPLOAD_TRACKERS | TABLE | 25 | This table tracks the state of files being uploaded for Attachments using a background process, whic... |
| FND_FORM_FUNCTIONS | TABLE | 16 | Stores Functions also referred to as Actions or Privileges |
| FND_FORM_FUNCTIONS_BK | TABLE | 13 | Stores Form Functions backup data also referred to as Actions or Privileges |
| FND_FORM_FUNCTIONS_SB | TABLE | 7 |  |
| FND_FORM_FUNCTIONS_TL | TABLE | 16 | Stores Translatable attributes of Functions, which is also referred to as Actions or Privileges. |
| FND_FORM_FUNCTIONS_TL_BK | TABLE | 13 | Stores Translatable attributes of Functions, which is also referred to as Actions or Privileges. |
| FND_FUSION_SEARCH_KEYWORDS | TABLE | 11 | This table is created to store search keywords submitted by the logged in user in fusion apps when u... |
| FND_GRANTS | TABLE | 48 | Stores Data Security Grants which is nothing but an intersection of Grantee, Object, Instance Set an... |
| FND_GRANTS_BK | TABLE | 45 | Stores Data Security Grants backup data which is nothing but an intersection of Grantee, Object, Ins... |
| FND_GRANTS_SB | TABLE | 7 |  |
| FND_GUIDED_LEARNING_CFG | TABLE | 19 |  |
| FND_GUIDED_LEARNING_ROLES | TABLE | 9 |  |
| FND_HTTP_SERVICE_TICKETS | TABLE | 5 |  |
| FND_HTTP_TICKETS | TABLE | 6 | Table to store short-lifespan and one-time-use tickets |
| FND_INDUSTRIES_B | TABLE | 11 | FND_INDUSTRIES_B |
| FND_INDUSTRIES_TL | TABLE | 14 | Meaningful comment for Industries translation table |
| FND_INDUSTRY_IN_TERRITORY | TABLE | 12 |  |
| FND_ISO_LANGUAGES_B | TABLE | 12 | FND_ISO_LANGUAGES_B |
| FND_ISO_LANGUAGES_TL | TABLE | 14 | ISO Language Translation Table |
| FND_ISSUE_RECORDINGS | TABLE | 22 | This table is used to keep track of the issue recordings created by users. A row is created when the... |
| FND_KF_ADFBC_USAGES | TABLE | 18 | This table stores the key flexfield ADF entity usages. |
| FND_KF_ADFBC_USAGES_BK | TABLE | 16 | This table stores the key flexfield ADF entity usages. |
| FND_KF_BOSS_USAGES | TABLE | 16 | This table stores the key flexfield BOSS business object usages. |
| FND_KF_CROSS_VAL_RULES | TABLE | 19 | Flexfields: Key Flexfields: Cross Validation Rules Table |
| FND_KF_CROSS_VAL_RULES_BK | TABLE | 17 | Flexfields: Key Flexfields: Cross Validation Rules Table |
| FND_KF_ESS_FILTERS | TABLE | 12 |  |
| FND_KF_FLEXFIELDS_B | TABLE | 30 | Flexfields: Key Flexfields: Key Flexfield Registration (_B) Table. |
| FND_KF_FLEXFIELDS_B_BK | TABLE | 28 | Flexfields: Key Flexfields: Key Flexfield Registration (_B) Table. |
| FND_KF_FLEXFIELDS_TL | TABLE | 15 |  |
| FND_KF_FLEXFIELDS_TL_BK | TABLE | 13 |  |
| FND_KF_LABELED_SEGMENTS | TABLE | 12 |  |
| FND_KF_LABELED_SEGMENTS_BK | TABLE | 10 |  |
| FND_KF_SEGMENTS_B | TABLE | 18 | Flexfields: Key Flexfields: Segment (_B) table. |
| FND_KF_SEGMENTS_B_BK | TABLE | 16 | Flexfields: Key Flexfields: Segment (_B) table. |
| FND_KF_SEGMENTS_TL | TABLE | 17 |  |
| FND_KF_SEGMENTS_TL_BK | TABLE | 15 |  |
| FND_KF_SEGMENT_INSTANCES | TABLE | 21 | Flexfields: Key Flexfields: Segment Instance Table. |
| FND_KF_SEGMENT_INSTANCES_BK | TABLE | 19 | Flexfields: Key Flexfields: Segment Instance Table. |
| FND_KF_SEGMENT_LABELS_B | TABLE | 16 |  |
| FND_KF_SEGMENT_LABELS_B_BK | TABLE | 14 |  |
| FND_KF_SEGMENT_LABELS_TL | TABLE | 16 |  |
| FND_KF_SEGMENT_LABELS_TL_BK | TABLE | 14 |  |
| FND_KF_STRUCTURES_B | TABLE | 15 | Flexfields: Key Flexfields: Structure (_B) Table. |
| FND_KF_STRUCTURES_B_BK | TABLE | 13 | Flexfields: Key Flexfields: Structure (_B) Table. |
| FND_KF_STRUCTURES_TL | TABLE | 16 |  |
| FND_KF_STRUCTURES_TL_BK | TABLE | 14 |  |
| FND_KF_STR_INSTANCES_B | TABLE | 19 | Flexfields: Key Flexfields: Structure Instance (_B) Table. |
| FND_KF_STR_INSTANCES_B_BK | TABLE | 17 | Flexfields: Key Flexfields: Structure Instance (_B) Table. |
| FND_KF_STR_INSTANCES_TL | TABLE | 16 |  |
| FND_KF_STR_INSTANCES_TL_BK | TABLE | 14 |  |
| FND_KF_TABLE_USAGES | TABLE | 19 | Flexfields: Key Flexfields: Table Usages table. |
| FND_KF_TABLE_USAGES_BK | TABLE | 17 | Flexfields: Key Flexfields: Table Usages table. |
| FND_KF_VALUE_ATTRS_B | TABLE | 18 | Flexfields: Key Flexfields: Value Attribute (_B) Table. |
| FND_KF_VALUE_ATTRS_B_BK | TABLE | 16 | Flexfields: Key Flexfields: Value Attribute (_B) Table. |
| FND_KF_VALUE_ATTRS_TL | TABLE | 17 |  |
| FND_KF_VALUE_ATTRS_TL_BK | TABLE | 15 |  |
| FND_KF_VRULES | TABLE | 16 | Flexfields: Key Flexfields: VRules table. |
| FND_KF_VRULES_BK | TABLE | 14 | Flexfields: Key Flexfields: VRules table. |
| FND_LABEL | TABLE | 17 | This table holds Labels associated with a specific Tree Structure Data Source. |
| FND_LABEL_TL | TABLE | 16 | This table holds translatable information for Labels associated with a Tree Structure Data Source. |
| FND_LANGUAGES_B | TABLE | 22 | FND_LANGUAGES_B |
| FND_LANGUAGES_TL | TABLE | 12 | Languages Translation Table longer description |
| FND_LIBRARIES_B | TABLE | 13 | This a to store all the library details |
| FND_LIBRARIES_TL | TABLE | 10 | This is NLS table for the base table |
| FND_LIST_SEARCH_KEYWORDS | TABLE | 13 | This table is created to store list search keywords submitted by the logged in user in fusion apps w... |
| FND_LOOKUP_TYPES | TABLE | 21 |  |
| FND_LOOKUP_TYPES_BK | TABLE | 17 | Stores the backup data of Lookup Types. |
| FND_LOOKUP_TYPES_SB | TABLE | 8 |  |
| FND_LOOKUP_TYPES_TL | TABLE | 17 |  |
| FND_LOOKUP_TYPES_TL_BK | TABLE | 13 |  |
| FND_LOOKUP_VALUES_B | TABLE | 21 |  |
| FND_LOOKUP_VALUES_B_BK | TABLE | 17 | Stores Lookup Values backup data. |
| FND_LOOKUP_VALUES_TL | TABLE | 19 |  |
| FND_LOOKUP_VALUES_TL_BK | TABLE | 15 | Stores the back up Lookup Values TL data |
| FND_LOOKUP_VIEWS | TABLE | 16 |  |
| FND_LOOKUP_VIEWS_BK | TABLE | 12 | Stores the backup data for Lookup Views. |
| FND_MAPPING_CATEGORIES | TABLE | 13 |  |
| FND_MAPPING_ENTITIES | TABLE | 27 |  |
| FND_MAP_APP_MODULE | TABLE | 9 | To store information about application id in source mapped to module id in target |
| FND_MAP_ATTACH_DOCS | TABLE | 34 | To maintain the mapping of file attachments in the source to the corresponding one in the target. |
| FND_MAP_ATTACH_ENTITY | TABLE | 24 | To map specific business objects, which own attachments, available in the source to the correspondin... |
| FND_MAP_CURRENCIES | TABLE | 11 | Store mapping of currency codes in source to its corresponding ones in Fusion. |
| FND_MAP_DOCUMENT_SEQUENCES | TABLE | 13 | STORES MAP OF SOURCE DOCUMENT SEQUENCES TO THEIR CORRESPONDING DOCUMENT SEQUENCES IN TARGET. |
| FND_MAP_DOC_SEQUENCE_AUDIT | TABLE | 12 | STORES MAP OF SOURCE DOCUMENT SEQUENCES AND DOCUMENT SEQUENCE VALUES. |
| FND_MAP_DOC_SEQUENCE_CATS | TABLE | 14 | STORES MAP OF SOURCE DOCUMENT SEQUENCE CATEGORIES TO THEIR CORRESPONDING DOCUMENT SEQUENCE CATEGORIE... |
| FND_MAP_DOC_SEQUENCE_USERS | TABLE | 13 | STORES MAP OF SOURCE USER DEFINED DOCUMENT SEQUENCES. |
| FND_MAP_DOC_SEQ_ASSIGNMENTS | TABLE | 13 | STORES MAP OF SOURCE DOCUMENT SEQUENCE ASSIGNMENTS TO THEIR CORRESPONDING DOCUMENT SEQUENCE ASSIGNME... |
| FND_MAP_FLEX_DFF | TABLE | 20 | Stores primary information about descriptive flexfields defined in source and their corresponding on... |
| FND_MAP_FLEX_DFF_COLUMNS | TABLE | 19 | Stores map information about descriptive flexfield context-specific columns in source and its corres... |
| FND_MAP_FLEX_DFF_CONTEXTS | TABLE | 15 | Table to map context values of Descriptive Flex Fields from EBS to Fusion |
| FND_MAP_FLEX_EFF_CATEGORIES | TABLE | 21 | Stores map information about Extendsible Flexfield Categories in source and its corresponding ones d... |
| FND_MAP_FLEX_EFF_USAGES | TABLE | 17 | Stores map information about Extendsible Flexfield usagesin source and its corresponding ones define... |
| FND_MAP_FLEX_KFF | TABLE | 17 | Stores information about mapping key flexfields in source to their corresponding ones in Fusion |
| FND_MAP_FLEX_KFF_COLUMNS | TABLE | 19 | Stores information about key flexfield columns in source mapped to its corresponding ones in Fusion |
| FND_MAP_INDUSTRIES | TABLE | 13 | Stores information about industry codes defined in source and their corresponding ones in Fusion |
| FND_MAP_ISO_LANGUAGES | TABLE | 14 | Maintains information about ISO language codes defined in source and their corresponding one in Fusi... |
| FND_MAP_LABEL | TABLE | 22 | Interface table for staging hierachy label information of both source and target. |
| FND_MAP_LANGUAGES | TABLE | 12 | To store map of languages defined in source (AU) and its corresponding in targer (Fusion). |
| FND_MAP_LOOKUPS | TABLE | 17 | Stores map of source lookup types and codes to their corresponding lookup types and codes in target. |
| FND_MAP_MERGE_FLEX_DFF | TABLE | 16 |  |
| FND_MAP_NATURAL_LANGUAGES | TABLE | 11 | Stores information about natural language codes defined in source and their corresponding ones in Fu... |
| FND_MAP_PROFILE_CATS | TABLE | 14 | STORES MAP OF SOURCE PROFILE CATEGORIES TO THEIR CORRESPONDING PROFILE CATEGORIES IN TARGET. |
| FND_MAP_PROFILE_OPTIONS | TABLE | 13 | STORES MAP OF SOURCE PROFILE OPTION IDS TO THEIR CORRESPONDING PROFILE OPTION IDS IN TARGET. |
| FND_MAP_SETID_REF_GROUPS | TABLE | 13 | To maintain the mapping to record group identifier in source to its corresponding reference group na... |
| FND_MAP_TERRITORIES | TABLE | 11 | Stores information about territory codes defined in source and their corresponding ones in Fusion. |
| FND_MAP_TIMEZONES | TABLE | 11 | Stores information of timezone codes defined in source and their corresponding one in Fusion |
| FND_MAP_TREE | TABLE | 19 | Interface table for staging Tree hierachy information. |
| FND_MAP_TREE_NODE | TABLE | 49 | Interface table for staging Tree hierachy information of both source and target. |
| FND_MENUS | TABLE | 14 | Stores Menu information, which is also referred to as Aggregate Privilege. The privileges contained ... |
| FND_MENUS_BK | TABLE | 11 | Stores Menu backup information, which is also referred to as Aggregate Privilege. The privileges con... |
| FND_MENUS_SB | TABLE | 7 |  |
| FND_MENUS_TL | TABLE | 16 | Stores the translatable attributes of a Menu also referred to as Aggregate Privilege. |
| FND_MENUS_TL_BK | TABLE | 13 | Stores backup data of the translatable attributes of a Menu also referred to as Aggregate Privilege. |
| FND_MENU_ENTRIES | TABLE | 14 | Stores privileges that are grouped to form an Aggregate Privilege. |
| FND_MENU_ENTRIES_BK | TABLE | 11 | Stores privileges backup data that are grouped to form an Aggregate Privilege. |
| FND_MESSAGES_B | TABLE | 20 | This table contains message dictionary messages. |
| FND_MESSAGES_B_BK | TABLE | 16 | This table contains message dictionary messages. |
| FND_MESSAGES_B_SB | TABLE | 8 |  |
| FND_MESSAGES_TL | TABLE | 20 |  |
| FND_MESSAGES_TL_BK | TABLE | 17 |  |
| FND_MESSAGE_TOKENS | TABLE | 16 |  |
| FND_MESSAGE_TOKENS_BK | TABLE | 12 |  |
| FND_METRICS_BACKLOG | TABLE | 14 |  |
| FND_MULTI_LINK_RECENT_ITEMS | TABLE | 33 |  |
| FND_NATURAL_LANGUAGES_B | TABLE | 13 | FND_NATURAL_LANGUAGES_B |
| FND_NATURAL_LANGUAGES_TL | TABLE | 14 | FND_NATURAL_LANGUAGES_TL |
| FND_NODE | TABLE | 11 | This table is a generic data source for Nodes. It is typiclaly used for tree-only nodes i.e., nodes ... |
| FND_NODE_TL | TABLE | 12 | This table holds the translatable attributes of Nodes. |
| FND_NOTIF_DEVICE_TOKENS | TABLE | 12 |  |
| FND_NTF_APP_MODULE | TABLE | 11 | Entity for managing external client application module registrations along with all their identifier... |
| FND_NTF_APP_MODULE_CHNL | TABLE | 21 | Entity for managing application module level defaults for the channel specific properties. |
| FND_NTF_CHANNEL | TABLE | 7 | Entity for centrally managing external channels supported by RIS Notifications. Seed Table. |
| FND_NTF_EVENT | TABLE | 15 | Entity for persisting business events received from all registered ApplicationModules. |
| FND_NTF_EVENT_RECIPIENT | TABLE | 10 | Entity for persisting receiver details for the business event. |
| FND_NTF_NOTIFICATION | TABLE | 27 | Entity for persisting the notification pertaining to the business event. |
| FND_NTF_NOTIFICATION_PL | TABLE | 8 | Entity for optionally persisting the generated delivery payloads for the outbound channels. |
| FND_NTF_RECIPIENT | TABLE | 11 | Table for caching the recipients preferences |
| FND_NTF_RECIPIENT_CHNL | TABLE | 24 | Entity for managing user specific values for the channel specific properties. |
| FND_NTF_TRANSFORM | TABLE | 27 | The table is used for storing transform entity. |
| FND_NTF_TRANSFORM_RESOURCE | TABLE | 8 | This table is used for storing transform resource entity. |
| FND_OBJECTS | TABLE | 30 | Stores the object defintion of the object (table or view) that needs to be secured. |
| FND_OBJECTS_BK | TABLE | 27 | Stores the backup data of object defintion of the object (table or view) that needs to be secured. |
| FND_OBJECTS_SB | TABLE | 7 |  |
| FND_OBJECTS_TL | TABLE | 16 | Stores the translatable attributes of Objects that are secured. |
| FND_OBJECTS_TL_BK | TABLE | 13 | Stores the backup data of translatable attributes of Objects that are secured. |
| FND_OBJECT_INSTANCE_SETS | TABLE | 18 | Stores the Object Instance Sets that corresponds to an Object. Object Instance Set is nothing but a ... |
| FND_OBJECT_INSTANCE_SETS_BK | TABLE | 15 | Stores the backup data of Object Instance Sets that corresponds to an Object. Object Instance Set is... |
| FND_OBJECT_INSTANCE_SETS_TL | TABLE | 17 | Stores the translatable attributes of an Instance Set. |
| FND_OBJECT_INSTANCE_SETS_TL_BK | TABLE | 14 | Stores the backup data translatable attributes of an Instance Set. |
| FND_PILLAR_INSTANCE_B | TABLE | 8 |  |
| FND_PILLAR_INSTANCE_TL | TABLE | 11 |  |
| FND_PILLAR_MAPPING | TABLE | 9 | FND_PILLAR_MAPPING |
| FND_PILLAR_TOPOLOGY_OPTIONS_B | TABLE | 8 |  |
| FND_PILLAR_TOPOLOGY_OPTIONS_TL | TABLE | 10 |  |
| FND_PRODUCT_FAMILY_DOMAIN_MAP | TABLE | 11 |  |
| FND_PROFILE_CATS_B | TABLE | 13 | Stores Profile (Option) Categories |
| FND_PROFILE_CATS_TL | TABLE | 15 | Translations for FND_PROFILE_CATS |
| FND_PROFILE_CAT_OPTIONS_B | TABLE | 14 | Intersection table between FND_PROFILE_OPTIONS and FND_PROFILE_CATS |
| FND_PROFILE_HIERARCHIES | TABLE | 11 |  |
| FND_PROFILE_HIERARCHY_LEVELS | TABLE | 12 | FND_PROFILE_HIERARCHY_LEVELS is used to maintain the profile levels that are applicable. Currently w... |
| FND_PROFILE_LEVELS | TABLE | 15 | FND_PROFILE_LEVELS allows you to dynamically define all the levels support by the Application. |
| FND_PROFILE_OPTIONS_B | TABLE | 19 | FND_PROFILE_OPTIONS_B meaningful comment |
| FND_PROFILE_OPTIONS_TL | TABLE | 14 | FND_PROFILE_OPTIONS_TL meaningful comment |
| FND_PROFILE_OPTION_LEVELS | TABLE | 14 | Profile option levels table comment |
| FND_PROFILE_OPTION_VALUES | TABLE | 14 | FND_PROFILE_OPTION_VALUES stores the profile option values for a particiular level value. |
| FND_RAND_STATES | TABLE | 37 | This table stores the state information used by the secure pseudo random number generator |
| FND_RDS_B | TABLE | 9 | This table is for stroing Report Delivery Service needed by provisioning |
| FND_RDS_PILLAR_DATA_USAGE | TABLE | 9 | This table is to store RDS and consumer map |
| FND_RDS_PILLAR_TPLGY_MAP | TABLE | 11 |  |
| FND_RDS_TL | TABLE | 10 | This is the translatable table for fnd_rds |
| FND_RECENT_ITEMS_LIST | TABLE | 33 | This table is created to store recent items belonging to the logged in user in fusion apps. |
| FND_RM_EXEMPT | TABLE | 3 |  |
| FND_ROLE_MIGRATION_COMPLETED | TABLE | 13 |  |
| FND_ROLE_MIGRATION_RETRY | TABLE | 18 |  |
| FND_RRA_ADDRS | TABLE | 19 | This table will store addresses |
| FND_RRA_COUNTRIES | TABLE | 8 | This table will store ISO country codes and names |
| FND_RRA_CURRENCIES | TABLE | 16 | This table will store diffferent currencies |
| FND_RRA_CURR_CONV_RATES | TABLE | 12 | This table will store daily conversion rates between diffferent currencies |
| FND_RRA_CUSTOMERS | TABLE | 15 | This table will store customer details |
| FND_RRA_CUSTOMER_ADDRESSES | TABLE | 18 | This table will store customer addresses details |
| FND_RRA_CUSTS | TABLE | 14 | This table will store customer details |
| FND_RRA_ODRS | TABLE | 25 | This table will store order details |
| FND_RRA_ODR_LINES | TABLE | 16 | This table will store order lines details |
| FND_RRA_ORDERS | TABLE | 17 | This table will store orders details |
| FND_RRA_ORDER_LINES | TABLE | 14 | This table will store order lines details |
| FND_RRA_PRODS | TABLE | 23 | This table will store products details |
| FND_RRA_PRODUCTS | TABLE | 25 | This table will store products details |
| FND_RRA_PRODUCT_CATEGORIES | TABLE | 9 | This table will store product category details |
| FND_RRA_PROD_CATS | TABLE | 10 | This table will store product category details |
| FND_RRA_SHIP_METHODS | TABLE | 13 | This table will store order shipping methods |
| FND_RRA_STORE_PRODS | TABLE | 27 | This table will store products stocked by the store, also referred to as the store-front inventory |
| FND_RRA_SUPPLIERS | TABLE | 14 | This table will store suppliers details |
| FND_RRA_SUPPLIERS_PRODUCTS | TABLE | 16 |  |
| FND_RRA_SUPPLIER_INVENTORY | TABLE | 18 |  |
| FND_RRA_SUPPLIER_SITES | TABLE | 19 |  |
| FND_RRA_SUPPS | TABLE | 13 | This table will store suppliers details |
| FND_RRA_SUPPS_PRODS | TABLE | 24 | This table will store products stocked by supplier, also referred to as the supplier inventory |
| FND_RRA_SUPP_SITES | TABLE | 10 | This table will store supplier site details |
| FND_RRA_TRAIN | TABLE | 11 | This table will store training details |
| FND_RRA_TRAINING | TABLE | 12 | This table will store training details |
| FND_RRA_TRAINING_TASKS | TABLE | 14 |  |
| FND_RRA_TRAINING_TASK_RELS | TABLE | 10 |  |
| FND_RRA_TRAIN_TASKS | TABLE | 13 | This table will store training task details |
| FND_RRA_TRAIN_TASK_RELS | TABLE | 9 | This table will store the relationships between training tasks |
| FND_RRA_USER_TRAINING | TABLE | 13 |  |
| FND_RRA_USER_TRAINING_TASKS | TABLE | 14 |  |
| FND_RRA_USR_TRAIN | TABLE | 12 | This table will store the training details for a particular user |
| FND_RRA_USR_TRAIN_TASKS | TABLE | 13 | This table will store the training task details for a particular user |
| FND_SAVED_SEARCH_B | TABLE | 26 | The primary table for storing Saved Searches. |
| FND_SAVED_SEARCH_TL | TABLE | 13 | Stores Translatable attributes for Fusion Saved Searches. |
| FND_SAVED_SEARCH_USER_DFLT | TABLE | 9 | This table captures the current default saved search for a user. This value overrides any defaulting... |
| FND_SAVED_SEARCH_USER_PREFS | TABLE | 10 | Table to store the user customizations (preferences) for a particular saved search. |
| FND_SEARCH_ATTACHMENT | TABLE | 9 |  |
| FND_SEARCH_ATTACHMENT_DETAILS | TABLE | 15 |  |
| FND_SEARCH_ATTACH_CONT | TABLE | 16 | Table for storing ContentTypes and their configuration for OSCS crawling. |
| FND_SEARCH_BULK_BOSS_SYNC | TABLE | 20 |  |
| FND_SEARCH_BULK_IMPORT | TABLE | 26 |  |
| FND_SEARCH_ERROR_RECORDS | TABLE | 26 |  |
| FND_SEARCH_INDEX_METADATA | TABLE | 26 |  |
| FND_SEARCH_LOG | TABLE | 11 |  |
| FND_SEARCH_OPTIONS_B | TABLE | 44 | The primary table storing Fusion Search Options. These options are passed to Oracle Fusion Search (G... |
| FND_SEARCH_OPTIONS_TL | TABLE | 17 | Stores Translatable attributes for Fusion Search Options. These options are passed to Oracle Fusion ... |
| FND_SEARCH_RESULTS | TABLE | 15 |  |
| FND_SEARCH_SMART_METADATA | TABLE | 13 | Registration of Applcore Smart Searches for OSCS Search Service and the Smart Search UI. |
| FND_SEARCH_TEMPLATE | TABLE | 14 | Registration of Applcore Index templates for OSCS Search Service and the Smart Search UI. |
| FND_SEARCH_VIEW_OPTIONS | TABLE | 13 | A Mapping table that identifies the GlobalSearchOptions for a given View Id. |
| FND_SECURITY_REPORT | TABLE | 4 |  |
| FND_SELECTED_ROLES | TABLE | 12 |  |
| FND_SESSIONS | TABLE | 28 | This table contains the sessions that are created when users sign into the applications. It is meant... |
| FND_SESSION_ATTRIBUTES | TABLE | 7 | This table contains information about the attributes of the sessions stored in the parent sessions t... |
| FND_SESSION_NAMESPACES | TABLE | 4 | This table contains the namespaces of the sessions stored in the parent sessions table. Each namespa... |
| FND_SESSION_ROLE_SETS | TABLE | 5 | This table contains combinations of roles formed as sets, which are associated with users who have s... |
| FND_SESSION_TEMPLATES | TABLE | 17 | This table contains templates for the sessions that are created when users sign into the application... |
| FND_SESSION_USERS | TABLE | 4 | This table contains the user name and user ID of every user that has signed into the applications. I... |
| FND_SESSION_USER_ACTIVITY | TABLE | 6 | This table tracks UI activity for the given user. |
| FND_SETID_ASSIGNMENTS | TABLE | 13 | This table contains details of the reference data sets that are assigned to reference groups, based ... |
| FND_SETID_REFERENCE_ENTITIES | TABLE | 14 | The FND_SETID_REFERENCE_ENTITIES table captures all reference entities in each reference group. |
| FND_SETID_REFERENCE_GROUPS_B | TABLE | 13 | The FND_SETID_REFERENCE_GROUPS_B table captures the default determinant type for all reference entit... |
| FND_SETID_REFERENCE_GROUPS_TL | TABLE | 14 | This table contains the translations of all reference groups stored in REFERENCE_GROUP_NAME. |
| FND_SETID_SETS | TABLE | 15 | This table contains reference data sets that are shared across organizations, Reference data sets co... |
| FND_SETID_SUMMARY | TABLE | 17 | This is fnd_setid_summary table |
| FND_SETUP_DATA_ACTIONS | TABLE | 8 | This table stores the rules for certain actions and features. |
| FND_SP_SUGGESTIONS | TABLE | 10 | Suggestions Service is a Helidon MP based Smart Platform micro service being developed as part of Sa... |
| FND_SRS_MASTER | TABLE | 8 |  |
| FND_STATS_BS_IGNORE_TABS | TABLE | 1 |  |
| FND_STATS_BS_LOG | TABLE | 7 |  |
| FND_STR_DEPLOYMENTS | TABLE | 7 | Table to store the APM deployment states and delta deployment details |
| FND_STR_DEPLOYMENT_CACHE | TABLE | 7 | Table to store strings -i18n.json artifacts for APM deployments. |
| FND_SUGGEST_GROUPS_B | TABLE | 19 | Definition of Search Suggest Groups as used by Global Search. |
| FND_SUGGEST_GROUPS_TL | TABLE | 15 | Stores Translatable attributes for Fusion Suggest Groups. These options are passed to Oracle Fusion ... |
| FND_SUIS_APEX_ACVN | TABLE | 15 |  |
| FND_SUIS_APEX_ACVN_RESULT | TABLE | 8 |  |
| FND_SUIS_APEX_LOG_TRACKER | TABLE | 8 |  |
| FND_SYNONYMS_B | TABLE | 16 | The primary table for storing Fusion Synonyms. |
| FND_SYNONYMS_TL | TABLE | 22 | The primary table for storing Fusion Synonyms. |
| FND_TABLE_DATASHAPES | TABLE | 12 | This table will be used to maintain the Table level Datashape Info for all Fusion Tables. It will st... |
| FND_TERRITORIES_B | TABLE | 22 | FND_TERRITORIES_B |
| FND_TERRITORIES_TL | TABLE | 14 | Territories translation table comment |
| FND_TIMEZONES_B | TABLE | 16 | Timezone table much longer comment |
| FND_TIMEZONES_TL | TABLE | 13 | Timezone translation table longer comment |
| FND_TREE | TABLE | 13 | This table holds Trees details for managing trees. |
| FND_TREE_AUDIT_JOB | TABLE | 15 | Stores information for Auditing of Trees scheduldedas batch mode job. |
| FND_TREE_DATA_SOURCE_PARAMS | TABLE | 14 | This table holds values for Tree Structure Data Source Parameters for a specific Tree. |
| FND_TREE_FLATTENING_HISTORY | TABLE | 11 | This table holds records of tree flattening history. |
| FND_TREE_LABEL | TABLE | 19 | Th table holds Tree Labels i.e., Labels associated with a specific Tree. |
| FND_TREE_LOG | TABLE | 11 | This table holds records of tree node operations. |
| FND_TREE_LOG_PARAMS | TABLE | 9 | This table holds parameters for each tree node operation entry. |
| FND_TREE_NODE | TABLE | 38 | This table holds the nodes of trees. |
| FND_TREE_NODE_CF | TABLE | 235 | This table holds column flattened Tree Nodes. |
| FND_TREE_NODE_RF | TABLE | 28 | This table holds row flattened representations of Tree Nodes. |
| FND_TREE_STRUCTURE | TABLE | 35 | This table defines a Tree Structure. |
| FND_TREE_STRUCTURE_TL | TABLE | 14 | This table holds translatable attributes of Tree Structures. |
| FND_TREE_TL | TABLE | 15 | This table holds the translatable attributes of Trees. |
| FND_TREE_VERSION | TABLE | 24 | This table holds Tree Versions. |
| FND_TREE_VERSION_AUDIT_RES | TABLE | 15 | Tree Version Audit Resoult storage for batch mode auditing of tree versions. |
| FND_TREE_VERSION_AUDIT_RES_TL | TABLE | 14 | Translatable information for tree version audit result table. |
| FND_TREE_VERSION_TL | TABLE | 17 | This table holds translatable attributes of Tree Versions. |
| FND_TS_DATA_SOURCE | TABLE | 30 | This table describes a Tree Structure Data Source. |
| FND_TS_DATA_SOURCE_PARAMS | TABLE | 16 | This table stores Tree Structure Data Source Parameters (if any). |
| FND_TS_DATA_SOURCE_REL | TABLE | 14 | This table holds the relationships between Tree Structure Data Sources. |
| FND_TS_DATA_SOURCE_TL | TABLE | 14 | This table holds translatable information for Data Source. |
| FND_USER_MIGRATION_COMPLETED | TABLE | 14 |  |
| FND_USER_MIGRATION_PARAMETERS | TABLE | 10 |  |
| FND_USER_MIGRATION_RETRY | TABLE | 20 |  |
| FND_USER_NAVIGATIONS | TABLE | 25 |  |
| FND_USER_PREFERENCES | TABLE | 5 |  |
| FND_USER_ROLES_ASSOCIATION | TABLE | 16 | Table for storing one record for each Role Membership that the user has been provisioned in LDAP. |
| FND_USER_ROLE_MIGRATION_DONE | TABLE | 13 |  |
| FND_USER_ROLE_MIGRATION_RETRY | TABLE | 18 |  |
| FND_VS_RELATED_SETS | TABLE | 13 | Flexfields: Value Sets: Related Value Sets. |
| FND_VS_RELATED_SETS_BK | TABLE | 11 | Flexfields: Value Sets: Related Value Sets. |
| FND_VS_RELATED_VALUES | TABLE | 15 | Flexfields: Value Sets: Related Values. |
| FND_VS_RELATED_VALUES_BK | TABLE | 13 | Flexfields: Value Sets: Related Values. |
| FND_VS_VALUES_B | TABLE | 56 | Flexfields: Value Sets: Value (_B) Table. |
| FND_VS_VALUES_B_BK | TABLE | 54 | Flexfields: Value Sets: Value (_B) Table. |
| FND_VS_VALUES_TL | TABLE | 15 | Flexfields: Value Sets: Value (_TL) Table. |
| FND_VS_VALUES_TL_BK | TABLE | 13 | Flexfields: Value Sets: Value (_TL) Table. |
| FND_VS_VALUE_SETS | TABLE | 37 | Flexfields: Value Sets: Value Set Definition Table. |
| FND_VS_VALUE_SETS_BK | TABLE | 35 | Flexfields: Value Sets: Value Set Definition Table. |
| FND_VS_VT_TABLE_BO_EXT | TABLE | 31 | Flexfields: Value Sets: Value Set Definition Extension Table for BOSS equivalent of Table Validated ... |
| FND_VS_VT_TABLE_BO_EXT_BK | TABLE | 29 | Flexfields: Value Sets: Value Set Definition Extension Table for BOSS equivalent of Table Validated ... |
| FND_VS_VT_TABLE_EXT | TABLE | 27 | Flexfields: Value Sets: Value Set Definition Extension (Validation Type 'TABLE') Table. |
| FND_VS_VT_TABLE_EXT_BK | TABLE | 25 | Flexfields: Value Sets: Value Set Definition Extension (Validation Type 'TABLE') Table. |
| FND_VS_VT_VO_EXT | TABLE | 14 | Flexfields: Value Sets: Value Set Definition Extension (Validation Type 'VIEW_OBJECT') Table. |
| FND_VS_VT_VO_EXT_BK | TABLE | 12 | Flexfields: Value Sets: Value Set Definition Extension (Validation Type 'VIEW_OBJECT') Table. |
| FND_WATCHDOG_LOGS | TABLE | 9 |  |
| FND_WLS_ACTIVE | TABLE | 5 |  |
| FUN_ADM_ATTRIBUTES_B | TABLE | 21 | This table stores attributes from target and refeference objects that can be used in attribute deriv... |
| FUN_ADM_ATTRIBUTES_TL | TABLE | 15 | This table stores translation details of attributes from target and refeference objects that can be ... |
| FUN_ADM_ATTR_ASSIGNMENTS | TABLE | 14 | This table contains the association between objects and attributes for both target and output attrib... |
| FUN_ADM_ENTITY_OBJECT_GROUPS | TABLE | 15 | This table contains information of an entity or group of entities of a business process flow for whi... |
| FUN_ADM_REFERENCE_OBJECTS | TABLE | 13 | This table contains tables and views that are associated to a target table. The attributes of refere... |
| FUN_ADM_RULE_CONDITIONS | TABLE | 22 | This table contains the conditions for attribute derivation rules. |
| FUN_ADM_TARGET_ATTRIBUTES | TABLE | 14 | This table contains the target attribute availble for the attribute derivation rule. |
| FUN_ADM_TARGET_ATTR_RULES | TABLE | 19 | This table contains detail of attribute derivation rules. |
| FUN_ADM_TARGET_TABLES | TABLE | 21 | This table contains the target object to which the attribute derivation rule output value will be po... |
| FUN_ALLOC_CONDITIONS | TABLE | 10 | This table contains the values selected for each component within a line of an allocation process st... |
| FUN_ALLOC_DETERMINANTS_B | TABLE | 12 | This table contains the different types of steps that are supported for an allocation process type. ... |
| FUN_ALLOC_DETERMINANTS_TL | TABLE | 14 | This tables contains the translated allocation process type components. |
| FUN_ALLOC_GROUP_CONTEXT | TABLE | 11 | This table contains the values for dimensions intended to be applied across a group of steps within ... |
| FUN_ALLOC_KEYWORDS | TABLE | 8 | This table contains the keywords that are currently or previously associated with an allocation proc... |
| FUN_ALLOC_KEYWORD_USAGE | TABLE | 10 | This table contains the keywords that are currently associated with an allocation process or allocat... |
| FUN_ALLOC_MODELS_B | TABLE | 11 | This table contains allocation models. |
| FUN_ALLOC_MODELS_TL | TABLE | 14 | This table contains the translated allocation models. |
| FUN_ALLOC_PROCESSES | TABLE | 18 | This table contains the properties of an allocation process, including the name, description, status... |
| FUN_ALLOC_PROCESS_EXEC_FLOW | TABLE | 11 | This table contains a copy of the relationships between the steps within an allocation process for a... |
| FUN_ALLOC_PROCESS_FLOW | TABLE | 11 | This table contains the relationships between the steps within an allocation process to display them... |
| FUN_ALLOC_PROCESS_SETS | TABLE | 10 | This table contains the properties of an allocation process set, including the name, description, an... |
| FUN_ALLOC_PROCESS_SET_ASSIGN | TABLE | 10 | This table contains the allocation processes that are included in an allocation process set. An allo... |
| FUN_ALLOC_PROCESS_TYPES_B | TABLE | 13 | This table contains the types of allocation processes for each allocation model. |
| FUN_ALLOC_PROCESS_TYPES_TL | TABLE | 14 | This table contains the translated allocation processes for each allocation model. |
| FUN_ALLOC_STEPS | TABLE | 19 | This table contains the properties of an allocation process step, including the name, description, t... |
| FUN_ALLOC_STEP_EXEC_HISTORY | TABLE | 19 | This table contains the status or result for each step of the allocation process that is processed. |
| FUN_ALLOC_STEP_LINES | TABLE | 9 | This table contains the lines for an allocation process step. |
| FUN_ALLOC_VARIABLES | TABLE | 12 | This table contains the properties of a variable, including the name, description, type, default val... |
| FUN_ALLOC_VARIABLE_SETS | TABLE | 11 | This table contains the variable sets. A variable set contains values for every variable used in an ... |
| FUN_ALLOC_VARIABLE_USAGE | TABLE | 9 | This table contains the steps within an allocation process to which a variable is assigned. |
| FUN_AV_METADATA | TABLE | 19 | To store all the metadata information about created analytical view. This table will be used interna... |
| FUN_AV_METADATA_DETAIL | TABLE | 31 | To store all the metadata detailed information about created analytical view. This table will be use... |
| FUN_BAL_ERRORS_T | TABLE | 24 | This is a temporary table which is used internally by Oracle. |
| FUN_BAL_HEADERS_T | TABLE | 17 | This is a temporary table which is used internally by Oracle. |
| FUN_BAL_INTER_ACCOUNTS_ADDL | TABLE | 14 | Intercompany accounts code combinations table for reconciliation report. |
| FUN_BAL_INTER_LE_BSV_MAP_T | TABLE | 27 | This is a temporary table which is used internally by Oracle. |
| FUN_BAL_INTER_RULES | TABLE | 25 | The table to hold the intercompany rules for balancing. |
| FUN_BAL_INTRA_LE_BSV_MAP_T | TABLE | 27 | This is a temporary table which is used internally by Oracle. |
| FUN_BAL_INTRA_RULES | TABLE | 21 | The intracompany balancing rules table contains information about ledger balancing options including... |
| FUN_BAL_LEDGERINT_LE_BSV_MAP_T | TABLE | 27 | This is a temporary table which is used internally by Oracle. |
| FUN_BAL_LINES_T | TABLE | 22 | This is a temporary table which is used internally by Oracle. |
| FUN_BAL_RECON_RESULT | TABLE | 17 | This table contains the total intercompany receivables and payables balance for a given ledger and a... |
| FUN_BAL_RESULTS_T | TABLE | 26 | This is a temporary table which is used internally by Oracle. |
| FUN_BATCH_DISTS | TABLE | 12 | This table contains the distribution details if a user has entered distributions using the automatic... |
| FUN_BC_APPLICATIONS | TABLE | 13 | This table stores blockchain applications. |
| FUN_BC_CONNECTIONS | TABLE | 26 | This table stores blockchain connection information. |
| FUN_BC_CONNECTION_TYPES | TABLE | 9 | This table stores the type of the blockchain connection. |
| FUN_BC_TRX_HISTORIES | TABLE | 20 | This table stores the execution histories of the transactions in blockchain network.The transactions... |
| FUN_BO_GROUP_MEMBERSHIP | TABLE | 10 | This table contains Spectra business objects mapping, object groups, and allowed actions on the obje... |
| FUN_BUSINESS_FUNCTIONS_B | TABLE | 13 | Setup functions a business unit can perform. |
| FUN_BUSINESS_FUNCTIONS_TL | TABLE | 14 | FUN_BUSINESS_FUNCTIONS_TL contains the translations of the prompts for Business Functions. |
| FUN_BUSINESS_OBJECT_GROUPS | TABLE | 9 | This table contains business object groups. |
| FUN_BUSINESS_OBJECT_MAPPING | TABLE | 16 | This table contains seeded mapping of Oracle Fusion Application actions, Spectra business objects, a... |
| FUN_BU_SERVICE_PROVIDERS | TABLE | 13 | FUN_BU_SERVICE_PROVIDERS stores Business Units client and provider relationship for a Business Funct... |
| FUN_BU_USAGES | TABLE | 9 | FUN_BU_USAGES stores the business functions that a business unit will perform |
| FUN_CATALOG_OBJECTS | TABLE | 18 | This table contains business object catalog. An object can be of three types: business objects, busi... |
| FUN_CATALOG_OBJECT_USAGES | TABLE | 21 | This table contains the usage of a business object for a consumer or consumption use case. Each cons... |
| FUN_CONT_EXEC_PROCESSES | TABLE | 14 | This table contains the metadata of processes enabled for continuous execution. |
| FUN_CONT_EXEC_WORK_ITEMS | TABLE | 14 | This table contains the work items need to be processed. |
| FUN_CONT_EXEC_WORK_ITEM_ATTRS | TABLE | 9 | This table contains the additional attributes related to the work item. |
| FUN_DATA_SLICES_B | TABLE | 22 | FUN_DATA_SLICES_B contains data slice definitions. Each data slice in your application is assigned a... |
| FUN_DATA_SLICES_TL | TABLE | 14 | FUN_DATA_SLICES_TL contains data slice name in installed languages. Each row includes the data slice... |
| FUN_DATA_SLICE_COLLECTION_B | TABLE | 17 | FUN_DATA_SLICE_COLLECTION_B contains source data definitions. This table has no foreign keys other t... |
| FUN_DATA_SLICE_COLLECTION_TL | TABLE | 14 | FUN_DATA_SLICE_COLLECTION_TL contains source data definition name in installed languages. Each row i... |
| FUN_DATA_SLICE_COLL_ASSIGNS | TABLE | 22 | FUN_DATA_SLICE_COLL_ASSIGNS contains data slices associated to a source data definition. Each associ... |
| FUN_DIST_LINES | TABLE | 27 | FUN_DIST_LINES stores the distributions for the Intercompany transactions. Both recipient and initia... |
| FUN_DOCIO_AL_ARTIFACTS | TABLE | 14 | This table contains transition data recognized and generated for each document, including elements s... |
| FUN_DOCIO_AL_EVENTS | TABLE | 16 | This table contains metadata associated with Adaptive Learning events, providing a comprehensive rec... |
| FUN_DOCIO_AL_MAPPINGS | TABLE | 15 | This table contains transformation mappings from source fingerprint to target structure, derived fro... |
| FUN_DOCIO_AL_RAGS | TABLE | 19 | This table constains Retrieval-Augmented Generation sources to help producing more accurate and cont... |
| FUN_DOCIO_AL_TRANSFORMS | TABLE | 12 | This table contains transformations learned from Adaptive Learning. The type of transformation varie... |
| FUN_DOCIO_FLOWS_B | TABLE | 25 | This table provides information about the seeded input and output flows of the document. The input a... |
| FUN_DOCIO_FLOWS_TL | TABLE | 14 | FUN_DOCIO_FLOWS_TL contains display name and description in installed languages for the seeded input... |
| FUN_DOCIO_FLOW_CONFIGS | TABLE | 11 | This table contains runtime configuration values for each input and output flow of the document. The... |
| FUN_DOCIO_FLOW_EXECUTIONS | TABLE | 22 | This table contains diagnostics and telemetry data for flow executions, providing real-time monitori... |
| FUN_DOCIO_FLOW_STEPS_B | TABLE | 18 | This table provides detailed information for each step within a specific input and output flow of th... |
| FUN_DOCIO_FLOW_STEPS_TL | TABLE | 13 | FUN_DOCIO_FLOW_STEPS_TL contains description in installed languages for the seeded input and output ... |
| FUN_DOCIO_FLOW_STEP_LDR_DTLS | TABLE | 23 | This table contains SQL Loader details for the input and output flows of the document, including con... |
| FUN_DOCIO_INCOMING_DOCUMENTS | TABLE | 15 | This table contains details of incoming documents, which are the documents received by input and out... |
| FUN_DOCIO_OUTGOING_DOCUMENTS | TABLE | 15 | This table contains details of outgoing documents, like acknowledgement, reports. |
| FUN_DOCIO_STEP_EXECUTIONS | TABLE | 19 | This table contains individual step execution details of a given flow.It provides real-time monitori... |
| FUN_DOCIO_STREAMS | TABLE | 17 | This table stores information about the channels supported by Document IO for processing business do... |
| FUN_DOCIO_STREAM_ASSOCIATIONS | TABLE | 10 | This table contains the associations between channels and flows, characterized by a many-to-many rel... |
| FUN_DOCIO_STREAM_CATEGORIES | TABLE | 18 | This table contains criteria for business conditions used to derive the seeded stream definition aro... |
| FUN_DOCIO_STREAM_DEFINITIONS | TABLE | 17 | This table contains criteria for stream definition along with its associated properties, including c... |
| FUN_DOCIO_TENANT_OPTIONS | TABLE | 12 | This table contains system-level configuration definitions. Configurations can be set as part of pro... |
| FUN_DOCIO_TRANSFORM_DOCUMENTS | TABLE | 26 | This table contains details of logical documents and transformed documents for a given incoming docu... |
| FUN_DS_DATA_ROLES_UPG_AUDIT | TABLE | 18 | This table contains information about the decomposition of generated data roles, their corresponding... |
| FUN_DS_DATA_ROLE_TMPL_AUDIT | TABLE | 14 | This table contains information about seeded data role templates and their seeded content. This is a... |
| FUN_DS_GRANTS_UPG_AUDIT | TABLE | 29 | This table contains grants information that maps to the identified data roles in the data role audit... |
| FUN_DS_USER_ROLES_UPG_AUDIT | TABLE | 10 | This table contains user role assignments information during upgrade. It is a persistent table. |
| FUN_EMAIL_IO_MESSAGES | TABLE | 20 | This table contains information for all inbound and outbound email messages processed by the system,... |
| FUN_EMAIL_IO_MSG_ATTACHMENTS | TABLE | 13 | This table contains binary content and metadata for files attached to email messages processed by th... |
| FUN_ENTITY_TAGS | TABLE | 20 | Captures the tags attached to business objects in FA |
| FUN_ERP_ATTACHMENT_CONTEXTS | TABLE | 21 | This table contains details associated with the predefined data for attachments. |
| FUN_ERP_BUSINESS_EVENTS | TABLE | 15 | This table contains the Business Events Metadata information. |
| FUN_ERP_SERVICE_EXECUTION_INFO | TABLE | 24 | This table contains details associated with the predefined data for ERP object services. |
| FUN_FRC_SEARCH_ENTITIES | TABLE | 23 | This table contains the entities for supporting enhanced search in financial reporting center. |
| FUN_IC_CUST_SUPP_MAP | TABLE | 11 | Intercompany customer and supplier assignments. |
| FUN_IMPORT_ERRORS | TABLE | 12 | This table contains import error rows. |
| FUN_IM_REQUEST_METRICS | TABLE | 15 | This table tracks instrumentation metrics for individual concurrent request runs. |
| FUN_INBOUND_FAILOVER | TABLE | 8 | This table stores the processing state with context information for the ERP inbound flow when an exc... |
| FUN_INBOUND_MONITORING | TABLE | 8 | This table stores the processing state with context information for each ERP inbound flow. The data ... |
| FUN_INTERCO_MASTER_DOCUMENTS | TABLE | 25 | This table contains information of master documents for the multitier intercompany flow. |
| FUN_INTERCO_ORGANIZATIONS | TABLE | 20 | This table contains the details of the intercompany organizations. |
| FUN_INTERCO_ORG_BSVS | TABLE | 18 | This table contains the details of the intercompany organization associations to balancing segment v... |
| FUN_INTERCO_SOURCE_DOCUMENTS | TABLE | 77 | This table contains information of the source documents corresponding to the source document groups. |
| FUN_INTERCO_SOURCE_DOC_GROUPS | TABLE | 31 | This table contains information of the source document groups corresponding to the master documents. |
| FUN_INTERCO_TRX_SOURCE_DOCS | TABLE | 66 | The table contains source document information to prepare and create intercompany transactions. |
| FUN_INTERCO_TRX_SOURCE_DOCS_T | TABLE | 13 | The table contains identifiers of source documents that are ready for intercompany transactions prep... |
| FUN_INTERCO_TXN_NUMBERING | TABLE | 10 | This table contains the last sequence value for a combination of provider and recipient organization... |
| FUN_IN_ERROR_ACTIONS | TABLE | 15 | This table stores recommended user actions associated with different exceptions from ERP inbound int... |
| FUN_IN_INGESTION_ERRORS | TABLE | 39 | This table stores errors that have occurred during ERP inbound flows. |
| FUN_OUTBOUND_CONSUMERS | TABLE | 19 | This table defines the properties of an outbound consumer type. |
| FUN_OUTBOUND_CONSUMER_INSTNCES | TABLE | 10 | This table contains runtime properties of an outbound consumer type. |
| FUN_PARALLEL_CHUNKS | TABLE | 18 | This table contains the details of the chunks that are created to breakup the candidate data for a p... |
| FUN_PARALLEL_CHUNK_DATA | TABLE | 20 | This table contains the candidate data for processing. The data is segmented by the chunk. |
| FUN_PARALLEL_REQUESTS | TABLE | 11 | This table contains details of the Enterprise Service Scheduler requests for each parallel run. |
| FUN_PARALLEL_RUNS | TABLE | 10 | This table contains details of each parallel run submitted for processing, along with the setup used... |
| FUN_PARALLEL_SETUP | TABLE | 18 | This table contains the default metadata for parallel runs, and run-specific metadata for parallel r... |
| FUN_PARALLEL_SETUP_JOBS | TABLE | 20 | This table contains details about the jobs in a parallel setup. |
| FUN_PARALLEL_SETUP_JOB_PARAMS | TABLE | 14 | This table contains details of the job parameters for the overall parallel setup. |
| FUN_PARALLEL_SETUP_JOB_PHASES | TABLE | 12 | This table contains information about the phases processed by a parallel job. |
| FUN_PARALLEL_SETUP_PHASES | TABLE | 31 | This table contains details of each phase of a parallel run. |
| FUN_PARALLEL_SETUP_PHASE_BINDS | TABLE | 15 | This table contains details of the bind variables in each SQL statement represented in the parallel ... |
| FUN_PARALLEL_SETUP_PHASE_CHILD | TABLE | 12 | This table contains details of the downstream phases for which an upstream phase produces data. |
| FUN_PARALLEL_SETUP_PHASE_SQLS | TABLE | 14 | This table contains information about each SQL statement invoked from a given phase, including its t... |
| FUN_PARALLEL_UNCHUNKED_DATA | TABLE | 32 | This table contains the candidate data for processing. This data has not yet been chunked for proces... |
| FUN_PERIOD_STATUSES | TABLE | 18 | FUN_PERIOD_STATUSES stores the Intercompany period statuses if an Intercompany calendar has been def... |
| FUN_PROCESS_EXEC_HISTORY | TABLE | 22 | This table contains the properties of each execution of an allocation process or allocation process ... |
| FUN_QRTZ_BLOB_TRIGGERS | TABLE | 10 | This table is used to store triggers as blobs (this is used when Quartz users create their own custo... |
| FUN_QRTZ_CALENDARS | TABLE | 9 | It stores Quartz calendar information as blobs. |
| FUN_QRTZ_CRON_TRIGGERS | TABLE | 11 | This table stores cron triggers, including cron expression and time zone information. |
| FUN_QRTZ_FIRED_TRIGGERS | TABLE | 21 | This table stores status information relating to triggers that have fired and the relevant execution... |
| FUN_QRTZ_JOB_DETAILS | TABLE | 18 | This table stores detailed information for every configured quartz Job. |
| FUN_QRTZ_JOB_LISTENERS | TABLE | 9 | This table stores information about configured job listeners. |
| FUN_QRTZ_LOCKS | TABLE | 8 | This table stores pessimistic lock information for the application (if pessimistic locking is used). |
| FUN_QRTZ_PAUSED_TRIGGER_GRPS | TABLE | 8 | This table is used to store the trigger groups that have been paused. |
| FUN_QRTZ_SCHEDULER_STATE | TABLE | 10 | This table is used to store a few pieces of information about the state of the Scheduler and other S... |
| FUN_QRTZ_SIMPLE_TRIGGERS | TABLE | 12 | This table stores simple triggers, including repeat count, internal, and number of times triggered. |
| FUN_QRTZ_SIMPROP_TRIGGERS | TABLE | 20 | This table stores properties associated with simple triggers. |
| FUN_QRTZ_TRIGGERS | TABLE | 23 | This table stores information about configured triggers. |
| FUN_QRTZ_TRIGGER_LISTENERS | TABLE | 9 | This table stores information about configured trigger listeners. |
| FUN_RAPID_DEFAULT_ACCOUNTS | TABLE | 14 | Stores the input xml files for Rapid Start |
| FUN_RAPID_START_FILES | TABLE | 8 | Stores the input xml files for Rapid Start |
| FUN_RELATED_FUNCTIONS | TABLE | 12 | FUN_RELATED_FUNCTIONS contains the upstream and downstream business functions. |
| FUN_ROLE_DATA_SECURITY_MAPPING | TABLE | 16 | This table contains details for each role to security context mapping, and the metadata to identify ... |
| FUN_SEGMENTATIONS | TABLE | 12 | Defines the business object, typically a dimension, that is being segmented. A dimension could be se... |
| FUN_SEGMENTATION_DETAILS | TABLE | 13 | Defines segmentation values (like tier 1, tier 2, etc), tag to be applied for the particular segment... |
| FUN_SENSORS_B | TABLE | 19 | This table stores the seed data of the sensor. The data includes the sensor code, the sensor type, t... |
| FUN_SENSORS_TL | TABLE | 14 | This table is to store the translation details of the fun_sensors_b base table |
| FUN_SENSOR_ACTIVE_SCHEDULES | TABLE | 12 | This table stores all the active sensor schedules to be executed. |
| FUN_SENSOR_FAULTS | TABLE | 10 | This table stores the fault details corresponding to each sensor instance task (if any). |
| FUN_SENSOR_INSIGHT_ACTN_HIST | TABLE | 11 | This table stores all user and system actions performed on insights for a detailed audit trail. |
| FUN_SENSOR_INSIGHT_DETAILS | TABLE | 11 | This table stores insight records for each security context where a rule condition was satisfied. |
| FUN_SENSOR_INSIGHT_RECIPIENTS | TABLE | 12 | This table stores the recipients of insights (users or roles), including the generated summaries and... |
| FUN_SENSOR_INSTANCES | TABLE | 11 | This table stores the sensor instance details of each sensor execution |
| FUN_SENSOR_INSTANCE_TASKS | TABLE | 16 | The table stores the sensor instance task details. Eg: BusinessCriteriaResolverTask, ActionHandlerTa... |
| FUN_SENSOR_SCHEDULES | TABLE | 18 | This table contains details of the sensor schedules. This is the primary table where the schedules a... |
| FUN_SENSOR_SIGNALS | TABLE | 9 | This table stores signal records generated when a monitoring rule condition is satisfied at a specif... |
| FUN_SENSOR_USAGES_B | TABLE | 16 | This table is to store the instantiation of the sensor. |
| FUN_SENSOR_USAGES_TL | TABLE | 14 | This table is to store the translation details of the fun_sensor_usages_b base table |
| FUN_SEQUENCE_SETTINGS | TABLE | 10 | FUN_SEQUENCE_SETTINGS contains the configuration settings for implementing sequencing in Oracle Fusi... |
| FUN_SEQ_ASSIGNMENTS | TABLE | 24 | This table contains the assignments of a sequence definition. |
| FUN_SEQ_CONTEXTS | TABLE | 22 | This table contains context information of a sequence definition. |
| FUN_SEQ_ENTITIES | TABLE | 12 | This table is used to store sequence definition. |
| FUN_SEQ_HEADERS | TABLE | 14 | This table contains the sequence definition. |
| FUN_SEQ_REQUESTS | TABLE | 9 | This column is used for internal processing only. |
| FUN_SEQ_RULES | TABLE | 17 | This table is used to store the sequencing rules pertaining to the applications on which sequencing ... |
| FUN_SEQ_VERSIONS | TABLE | 19 | This table contains the versions of a sequence definition. |
| FUN_SITUATION_CONTEXTS | TABLE | 13 | This table contains Oracle Fusion applications situation contexts. A situation is generated in Oracl... |
| FUN_SPM_SQL_BASELINES | TABLE | 15 | This table contains the state of baselines created through SQL plan management to associate an indiv... |
| FUN_SPM_SQL_INSTANCES | TABLE | 17 | This table contains the individual SQL statements that roll up into a master SQL statement. It conta... |
| FUN_SPM_SQL_MASTER | TABLE | 14 | This table contains the master code and description that is used to identify this group of related S... |
| FUN_SPM_SQL_PLAN_INSTANCES | TABLE | 16 | This table contains the plans that are available to all of the individual SQL statements that roll u... |
| FUN_STATISTIC_DEFNS | TABLE | 16 | This table holds the definition of a statistic that is to be recorded. |
| FUN_STATISTIC_GROUPS | TABLE | 18 | This table holds the high level instatnce of a set of statistics |
| FUN_STATISTIC_VALUES | TABLE | 36 | This tables holds the value of an indivdual statistic. |
| FUN_STREAMS_B | TABLE | 15 | This table contains options of functional processes with the specific business flow context. |
| FUN_STREAMS_TL | TABLE | 9 | This table provides multilingual support (MLS) for option of functional process. MLS enables you to ... |
| FUN_STREAM_NOTIFICATIONS | TABLE | 14 | This table contains mapping of functional process notification details. |
| FUN_STREAM_PARAMETERS_B | TABLE | 13 | This table contains functional process request parameter values. |
| FUN_STREAM_PARAMETERS_TL | TABLE | 9 | This table provides Multi Language Support (MLS) for options of functional process details. MLS enab... |
| FUN_STREAM_REQUESTS | TABLE | 22 | This table contains options of functional processes details with the execution information. |
| FUN_STREAM_STEPS_B | TABLE | 25 | This table contains options of functional process details with the execution information. |
| FUN_STREAM_STEPS_TL | TABLE | 9 | This table provides multilingual support (MLS) for options of functional process details. MLS enable... |
| FUN_STREAM_STEP_LINKS | TABLE | 18 | This table contains functional process step relationships. |
| FUN_STREAM_TYPES_B | TABLE | 29 | This table contains mapping of functional processes with the specific business flow context. |
| FUN_STREAM_TYPES_TL | TABLE | 12 | This table provides multilingual support (MLS) for each functional process. MLS enables you to store... |
| FUN_STREAM_TYPE_PARAMETERS_B | TABLE | 21 | This table contains functional process request parameter metadata. |
| FUN_STREAM_TYPE_PARAMETERS_TL | TABLE | 12 | This table provides Multi Language Support (MLS) for options of functional process details. MLS enab... |
| FUN_STREAM_TYPE_STEPS_B | TABLE | 32 | This table contains mapping of functional process details with the execution information. |
| FUN_STREAM_TYPE_STEPS_TL | TABLE | 12 | This table provides multilingual support (MLS) for each functional process details. MLS enables you ... |
| FUN_STREAM_TYPE_STEP_LINKS | TABLE | 18 | This table contains functional process step type relationships. |
| FUN_SVS_POLICIES | TABLE | 22 | This table contains Segment Value Security Policies and Conditions definitions. |
| FUN_SVS_USER_POLICY_ASGNMNTS | TABLE | 15 | This table contains mapping of users to rules based on the security context and access selection . |
| FUN_SYSTEM_OPTIONS | TABLE | 24 | This table contains setup options defined at the system level which apply across the entire applicat... |
| FUN_TEMP_STAT_GROUPS | TABLE | 18 | This table holds the high level instatnce of a set of statistics |
| FUN_TEMP_STAT_VALUES | TABLE | 36 | This tables holds the value of an indivdual statistic. |
| FUN_TLM_JOBS | TABLE | 12 | This table contains information of jobs which have been instrumented. Only these jobs data will be i... |
| FUN_TLM_SENSOR_LOGS | TABLE | 29 | This table contains information of sensors. A sensor is an activity that happens in a system where t... |
| FUN_TRANSFERS | TABLE | 13 | This is a temporary table that is used by the Intercompany Transfer to General Ledger, Intercompany ... |
| FUN_TRX_BATCHES | TABLE | 29 | This table contains information about the intercompany transaction batches. The BATCH_NUMBER and INI... |
| FUN_TRX_HEADERS | TABLE | 61 | This tables contains the transactions that make up an intercompany transaction batch. The INITIATOR_... |
| FUN_TRX_LINES | TABLE | 15 | FUN_TRX_LINES contains some line level information for an intercompany transaction. Each row in FUN_... |
| FUN_TRX_TYPES_B | TABLE | 16 | This table contains the intercompany transaction types defined. |
| FUN_TRX_TYPES_TL | TABLE | 11 | This table contains the translatable column details for the intercompany transaction types. |
| FUN_TRX_TYPE_AR_MAPS | TABLE | 15 | FUN_TRX_TYPE_AR_MAPS stores the mapping between the Intercompany transaction type and the Receivable... |
| FUN_USER_ROLE_DATA_ASGNMNTS | TABLE | 33 | This table contains the assignments of a user , role and data security context. |
| FUN_WF_ACTIONS | TABLE | 41 | This table contains data related to action(s) on rule. |
| FUN_WF_ACTION_REQUESTS | TABLE | 11 | This table contains the details of the terminal actions performed on financial-related workflow tran... |
| FUN_WF_ATTRIBUTES_B | TABLE | 17 | This table contains predefined data of the various attributes of any transaction object available fo... |
| FUN_WF_ATTRIBUTES_TL | TABLE | 13 | This translation table contains the transactional attribute display name to be shown on the user int... |
| FUN_WF_CONDITIONS | TABLE | 20 | This table contains data related to conditions used within pattern as part of approval rules configu... |
| FUN_WF_CONFIGURATIONS | TABLE | 15 | This table contains task features metadata for workflows. |
| FUN_WF_DATASETS | TABLE | 10 |  |
| FUN_WF_DATASET_ASSIGNEES | TABLE | 17 | This table contains assignee information required to evaluate the data set rule sheet of the workflo... |
| FUN_WF_FACTS_B | TABLE | 22 | This table contains the predefined JAVA facts of any workflow. |
| FUN_WF_FACTS_TL | TABLE | 13 | This translation table contains the workflow fact display name to be shown on the user interface. |
| FUN_WF_HISTORY | TABLE | 22 | FUN_WF_HISTORY contains the approval and rejection history of each submission that passes through th... |
| FUN_WF_HISTORY_LINES | TABLE | 16 | FUN_WF_HISTORY_LINES contains the approval and rejection history of each submission that passes thro... |
| FUN_WF_OBJECTS_B | TABLE | 12 | This table contains the predefined data of the various transactional objects available for approval ... |
| FUN_WF_OBJECTS_TL | TABLE | 13 | This translation table contains the workflow fact display name to be shown on the user interface. |
| FUN_WF_PARTICIPANTS | TABLE | 25 | This table contains participants created for the approval setup uploaded through UI or spreadsheet. |
| FUN_WF_PATTERNS | TABLE | 21 | This table contains data related to patterns used in approval rules configuration. |
| FUN_WF_ROUTING_INSTANCES | TABLE | 18 | This table contains details of rule evaluation service like execution time, routing results or error... |
| FUN_WF_RULES | TABLE | 31 | This table contains approval rule metadata and assignment information. |
| FUN_WF_RULES_LISTS | TABLE | 9 | List Id is the Identifer of each list created |
| FUN_WF_RULE_ASSIGNMENTS | TABLE | 14 | This table stores the mapping of rules to assigned users and roles, including inclusion and exclusio... |
| FUN_WF_RULE_UPLOADS | TABLE | 18 | This table contains data related to the spreadsheet uploads through which approval rules are created... |
| FUN_WF_STAGES | TABLE | 17 | This table contains approval stage data. Approval stage can be like invoice document approval stage ... |
| FUN_WF_TRANSACTION_ATTRS | TABLE | 22 | This table contains the transaction attribute names required for each workflow to be shown as a summ... |
| FUN_WF_UPLOAD_ERRORS | TABLE | 23 | This table contains data related to the errors occurred as part of spreadsheet upload through which ... |
| FUN_WORKFLOWS_B | TABLE | 15 | This base table contains predefined workflow data required to query the SOA MDS to access rule dicti... |
| FUN_WORKFLOWS_TL | TABLE | 13 | This translation table contains the workflow display name to be shown on the user interface. |
| FV_ACCOUNT_ATTRIBUTE_HEADERS | TABLE | 10 | This table stores the federal account attribute header records. |
| FV_ACCOUNT_ATTRIBUTE_LINES | TABLE | 12 | This table stores the federal account attribute line records. |
| FV_ATTR_SUPPL_RULE_ALLOCS | TABLE | 13 | This table stores the federal attribute supplemental rule allocation records. |
| FV_ATTR_SUPPL_RULE_FILTERS | TABLE | 15 | This table stores the federal attribute supplemental rule filter records. |
| FV_ATTR_SUPPL_RULE_HEADERS | TABLE | 10 | This table stores the federal attribute supplemental rule header records. |
| FV_ATTR_SUPPL_RULE_LINES | TABLE | 15 | This table stores the federal attribute supplemental rule line records. |
| FV_BC_CONTROL_SEGMENTS | TABLE | 18 | This table contains the budgetary control segments information defined for the budgetary control typ... |
| FV_BC_CONTROL_TYPES | TABLE | 36 | This table contains the budgetary control type definition that will be used to create federal contro... |
| FV_BE_LEVELS | TABLE | 15 | This table contains information for Budget Levels defined for a Ledger. |
| FV_BE_LEVEL_CTL_BUDGET | TABLE | 12 | This table stores the control budgets associated with the budget levels for a ledger. |
| FV_BE_LEVEL_OPTIONS | TABLE | 21 | This table contains budget level options information for a Ledger. |
| FV_BE_TRANSACTION_ACCOUNTS | TABLE | 13 | This table contains GL accounts assigned to the budget execution types that will be used when creati... |
| FV_BE_TRANSACTION_HEADERS | TABLE | 33 | This table contains budget transaction header information. |
| FV_BE_TRANSACTION_LINES | TABLE | 37 | This table contains budget transaction lines information. |
| FV_BE_TRANSACTION_TYPES | TABLE | 25 | This table contains information for budget execution transaction types that will be used when creati... |
| FV_CFG_AGENCY_LOCATIONS | TABLE | 13 | This table contains information about agency location codes defined for both internal and external a... |
| FV_CFG_USSGL_ACCOUNTS | TABLE | 16 | This table contains information about U.S. Standard General Ledger Accounts. |
| FV_CROSS_SERVICE_RECEIPTS_ALL | TABLE | 63 | This table contains staged Treasury IAI Collections File inbound records for cross-servicing collect... |
| FV_CTA_EXTRACT | TABLE | 47 | This table stores the CTA transactions |
| FV_CTA_FBWT_ACCT_DEFINITIONS | TABLE | 11 | This table stores the CTA FBWT Account Definitions. |
| FV_DATA_ACT_BALANCES_EXTRACT | TABLE | 162 | This table stores the calculated balance amount for the DATA Act Files. |
| FV_DATA_ACT_BAL_CALCS | TABLE | 16 | This table stores information about the calculations based on balance name. |
| FV_DATA_ACT_BAL_CALCS_USSGL | TABLE | 17 | This table stores information about the calculations based on USSGL accounts to process the balance. |
| FV_DATA_ACT_BAL_HEADERS | TABLE | 16 | This table stores information about DATA Act balance header attributes. |
| FV_DATA_ACT_DEF_CALCULATIONS | TABLE | 14 | This table stores information about the calculation for different amount codes. |
| FV_DATA_ACT_DEF_HEADERS | TABLE | 26 | This table stores information about DATA Act amount definition header and amount assignment attribut... |
| FV_DATA_ACT_DEF_USSGL_ACCTS | TABLE | 26 | This table stores information about USSGL accounts and the criteria to process the accounts. |
| FV_DATA_ACT_FILE_CRITERIA | TABLE | 12 | This table stores information about the federal attribute filter criteria used to generate a DATA Ac... |
| FV_DATA_ACT_FILE_SEQUENCES | TABLE | 14 | This table stores sequence information for each DATA Act file. |
| FV_DATA_ACT_REPORT_EXTRACT | TABLE | 109 | This table stores the data in the printable format. |
| FV_DATA_ACT_REPORT_SUMMARY | TABLE | 49 | This table stores the summarized amount for the CCID, Period_num, Period_year along with federal att... |
| FV_DATA_ACT_REP_TRX_ACTIVITY | TABLE | 58 | This table stores information about the transaction details from gl_je_headers and gl_je_lines for t... |
| FV_EXCEPTION_DETAILS | TABLE | 13 | Stores exception information during federal process. |
| FV_FEDERAL_ATTRIBUTES | TABLE | 16 | This table stores the federal attribute records. |
| FV_FINCHRG_GROUPS | TABLE | 9 | This table contains information about finance charge groups. |
| FV_FINCHRG_GROUP_CUST_CLASSES | TABLE | 10 | This table contains customer class information for finance charges. |
| FV_FINCHRG_GROUP_TYPES | TABLE | 12 | This table contains information about finance charge group types. |
| FV_FINCHRG_TYPES | TABLE | 23 | This table contains information about the finance charge types such as the type of finance charge, b... |
| FV_FINCHRG_TYPE_RATES | TABLE | 15 | This table contains information about the rate details for a charge type. |
| FV_GTAS_ATTRIBUTES | TABLE | 35 | This table stores attributes information for GTAS accounts. |
| FV_GTAS_DATA_ACT_REP_RUN | TABLE | 24 | This table stores information about GTAS and DATA Act file reporting parameters. |
| FV_GTAS_REPCODE_ALLOCATIONS | TABLE | 11 | This table stores the GTAS reporting code allocation records. |
| FV_GTAS_REPCODE_FILTERS | TABLE | 15 | This table stores the GTAS reporting code filter records. |
| FV_GTAS_REPCODE_HEADERS | TABLE | 12 | This table stores the GTAS reporting code header records. |
| FV_GTAS_REPCODE_LINES | TABLE | 12 | The table stores the GTAS reporting code line records. |
| FV_IPAC_TRANSACTION_DATA | TABLE | 98 | This table stores transaction details from IPAC broker system. |
| FV_LEDGER_GROUPS | TABLE | 25 | This table contains information on federal ledger groups. Ledger groups are defined for each GL key ... |
| FV_LEDGER_GROUP_BE_LEVELS | TABLE | 11 | This table contains information of budget levels defined for each ledger groups.The budget level nam... |
| FV_PARTY_TAS_REPORTS | TABLE | 17 | This table stores information about the party for which TAS was updated. |
| FV_PAYMENT_EXCLUSION_CRITERIAS | TABLE | 16 | This table contains payment offset exclusion criterias so that no payment netting will be done by tr... |
| FV_PAYMENT_FORMAT_MAPPINGS | TABLE | 13 | This table contains the payment format mapping configuration |
| FV_PAYMENT_REASON_CODES_ALL | TABLE | 14 | This table contains the interest and discount lost reason codes for an invoice. |
| FV_PAYMENT_SUMMARY_BY_TAS | TABLE | 11 | This table contains the payment summary by treasury symbol for reporting purpose. |
| FV_PAY_INVOICE_DUE_DATES | TABLE | 52 | This table stores the data that is required for reporting by the Prompt Payment Due Date Calculation... |
| FV_REPORTING_GTAS_BULK_EXTRACT | TABLE | 73 | This table stores GTAS bulk file balances for USSGL and federal attributes. |
| FV_REPORTING_TRX_ACTIVITY | TABLE | 75 | This table stores federal activity and attribute details. |
| FV_REPORTING_TRX_BALANCES | TABLE | 63 | This table stores transaction activity balances for federal attributes. |
| FV_SAM_ACCOUNT_ADDRESS_SETS | TABLE | 18 | This table stores information about Account Address Set and Customer Account assignment for a SAM Tr... |
| FV_SAM_BUSINESS_UNITS | TABLE | 17 | Stores Information about Business unit Assignment for SAM Trading Partners. |
| FV_SAM_TRADING_PARTNER | TABLE | 376 | This table stores information about SAM Trading Partners. |
| FV_SETUP_OPTIONS | TABLE | 18 | This table contains configuration options defined for each business units |
| FV_TRANSACTION_DOCUMENTS | TABLE | 9 | This table stores the information for the transaction documents. |
| FV_TREASURY_CHECK_NUM_RANGES | TABLE | 11 | This table contains treasury confirmation payment check ranges. |
| FV_TREASURY_CONFIRM_ACTION | TABLE | 13 | This table contains the actions performed against each treasury confirmation. |
| FV_TREASURY_CONFIRM_ALL | TABLE | 31 | This table contains payments confirmed in the treasury confirmation. |
| FV_TREASURY_OFFSET_AMOUNTS | TABLE | 13 | This table contains information on treasury confirmation payment off set amount. |
| FV_TROR_DETAILS | TABLE | 36 | This table contains detailed information about Treasury Report on Receivables (TROR) transactions. |
| FV_TROR_HEADERS | TABLE | 21 | This table contains header information about Treasury Report on Receivables (TROR) transactions. |
| FV_TR_BETC | TABLE | 17 | This table contains Treasury Business Event Type Code Information that need to be associated to Trea... |
| FV_TR_FED_ACCOUNT_SYMBOLS | TABLE | 15 | This table contains Federal U.S. Standard General Ledger Account Information. |
| FV_TR_FUND_ATTRIBUTES | TABLE | 26 | This table contains funds associated to a treasury symbol along with fund attributes. |
| FV_TR_TAS_BETC | TABLE | 10 | This table contains Business Event Type Code assignment for Treasury symbols' Symbols Information. |
| FV_TR_TREAS_ACCOUNT_SYMBOLS | TABLE | 27 | This table contains Treasury Account Symbols Information. |
| FV_USSGL_ACCOUNT_ATTRIBUTES | TABLE | 32 | This table contains information about U.S. Standard General Legder Accounts child table. |
| FV_XLA_TRANSACTION_LINES | TABLE | 62 | "This table contains the federal specific sources required during the federal subledger budgetary ac... |
| GL_ACCESS_SETS | TABLE | 17 | GL_ACCESS_SETS contains the definition of each data access set defined in the Data Access Set page. ... |
| GL_ACCESS_SET_ASSIGNMENTS | TABLE | 13 | GL_ACCESS_SET_ASSIGNMENTS contains the access privilege information for each data access set. Each r... |
| GL_ACCESS_SET_LEDGERS | TABLE | 12 | This table contains the access privilege information for each data access set. Each row includes the... |
| GL_ACCESS_SET_NORM_ASSIGN | TABLE | 22 | GL_ACCESS_SET_NORM_ASSIGN contains the access privilege information for each data access set. Each r... |
| GL_ACCOUNT_ALIASES_B | TABLE | 84 | GL_ACCOUNT_ALIAES_B stores information of account aliases that representing frequently used account ... |
| GL_ACCOUNT_ALIASES_TL | TABLE | 12 | GL_ACCOUNT_ALIASES_TL stores account alias names in installed languages. Each row includes the accou... |
| GL_ACCOUNT_GROUPS | TABLE | 20 | This table stores the groups of accounts setup by each user to enable easy monitoring of general led... |
| GL_ACCOUNT_GROUP_DEFAULT | TABLE | 12 | GL_ACCOUNT_GROUP_DEFAULT contains the default account group for user and access Set identifier combi... |
| GL_ACCOUNT_GROUP_DETAILS | TABLE | 103 | This table stores the individual accounts that comprise each account group. This enables easy monito... |
| GL_ACCOUNT_GROUP_USER_ASSIGN | TABLE | 9 | Stores the account group user assignments. |
| GL_ALLOC_RTP | TABLE | 16 | This column is used in internal processing only |
| GL_ALLOC_RULES | TABLE | 20 | GL_ALLOC_RULES contains Allocation Rules. |
| GL_ALLOC_RULESETS | TABLE | 11 | This column is used in internal processing only |
| GL_APPLICATION_GROUPS | TABLE | 11 | GL_APPLICATION_GROUPS replaces FND_APPLICATION_GROUPS. It holds rows for individual application prod... |
| GL_AUTOMATIC_POSTING_OPTIONS | TABLE | 15 | GL_AUTOMATIC_POSTING_OPTIONS contains the criteria used by the AutoPost Criteria Set program to sele... |
| GL_AUTOMATIC_POSTING_SETS | TABLE | 21 | GL_AUTOMATIC_POSTING_SETS contains the automatic posting sets you defined in the AutoPost Criteria S... |
| GL_AUTOREVERSE_OPTIONS | TABLE | 13 | GL_AUTOREVERSE_OPTIONS contains the automatic reversal options you define using the Reversal Criteri... |
| GL_AUTOREV_CRITERIA_SETS | TABLE | 10 | GL_AUTOREV_CRITERIA_SETS contains the journal reversal criteria sets you create using the Journal Re... |
| GL_AUTORUN_ERROR_ACTIONS | TABLE | 13 | This table stores recommended user actions associated with different accounting exceptions. |
| GL_AUTORUN_ERROR_CODES | TABLE | 13 | This table contains all of the detailed error codes that have been registered and their associated e... |
| GL_AUTORUN_LEDGER_EXCLUSIONS | TABLE | 8 | This table keeps track of the primary ledgers and ledger sets that are excluded from automation. The... |
| GL_AUTORUN_RUNS | TABLE | 12 | This table keeps track of each of the overall automation runs. |
| GL_AUTORUN_RUN_ERRORS | TABLE | 51 | This table keeps track of all of the system and validation errors that have occurred during the auto... |
| GL_AUTORUN_RUN_NOTIFY | TABLE | 11 | This table contains the specific ledger and error categories that will be processed by each report s... |
| GL_AUTORUN_RUN_NOTIFY_USERS | TABLE | 8 | This table contains which report submissions will be sent to each of the individual users for an aut... |
| GL_AUTORUN_RUN_REQUESTS | TABLE | 15 | This table keeps track of all of the requests that make up an automation run. |
| GL_AUTORUN_RUN_RESULTS | TABLE | 10 | This table contains the overall impact of the automation run. |
| GL_AUTORUN_SETUP | TABLE | 14 | This table keeps track of whether automation has been set up, and if so what the current settings ar... |
| GL_AUTORUN_SETUP_EXCLUSIONS | TABLE | 13 | This table keeps track of what journal sources should be excluded from automation. |
| GL_AUTORUN_SETUP_NOTIFY | TABLE | 11 | This table keeps track of who should be notified when issues occur for a specific ledger and error c... |
| GL_AUTORUN_SETUP_NOTIFY_USERS | TABLE | 9 | This table keeps track of the individual users who should be notified when issues occur for a specif... |
| GL_BALANCES | TABLE | 39 | GL_BALANCES contains actual, budget, and encumbrance balances for detail and summary accounts. This ... |
| GL_BALANCES_CUBES | TABLE | 56 | This table is used for internal processing only |
| GL_BALANCES_DELTA | TABLE | 30 | GL_BALANCES_DELTA is used only during internal processing. |
| GL_BALANCES_DELTA_INTERIM | TABLE | 24 | GL_BALANCES_DELTA_INTERIM is used to temporarily store data from the GL_BALANCES_DELTA table. This t... |
| GL_BALANCE_CURRENCIES | TABLE | 8 | GL_BALANCE_CURRENCIES is used only during internal processing. For each ledger, this table stores th... |
| GL_BALANCE_INIT_HISTORY | TABLE | 17 | This table stores the details from the balance initialization run, which creates opening balance jou... |
| GL_BALANCE_TRANSFER_HISTORY | TABLE | 27 | This is a temporary table which is used internally by Oracle. |
| GL_BAL_CUBE_CONCURRENCY | TABLE | 10 | GL_BAL_CUBE_CONCURRENCY contains information for a ledger if Oracle General ledger balances are not ... |
| GL_BUDGET_BALANCES | TABLE | 44 | This table stores general ledger budget balances (similar to the general ledger balances table - GL_... |
| GL_CALENDARS | TABLE | 28 | Unique identifier for accounting and commitment Calendars created in Oracle Fusion and has a one to ... |
| GL_CAL_CONFIRMED_YEARS | TABLE | 8 | This is a temporary table which is used internally by Oracle. |
| GL_CHART_OF_ACCOUNTS_OPTIONS | TABLE | 11 | This table contains general ledger options for a chart of accounts. |
| GL_COA_MAPPINGS | TABLE | 12 | GL_COA_MAPPINGS contains the chart of accounts mappings defined in the Chart of Accounts Mappings pa... |
| GL_COA_MAP_ACCOUNT_RULES | TABLE | 101 | GL_COA_MAP_ACCOUNT_RULES contains the account rules you define when you define a chart of accounts m... |
| GL_COA_MAP_MS_ROLLUP_RULES | TABLE | 13 | This table contains multi segment rollup rules of a chart of accounts mapping definition. |
| GL_COA_MAP_MULTI_SEG_RULES | TABLE | 14 | This table contains multi segment rules of a chart of accounts mapping definition. |
| GL_COA_MAP_ROLLUP_RULES | TABLE | 13 | GL_COA_MAP_ROLLUP_RULES contains the source segment ranges that you define in the Rollup Rules secti... |
| GL_COA_MAP_SEGMENT_RULES | TABLE | 14 | GL_COA_MAP_SEGMENT_RULES contains the rules you define in the Segment Rules region of the Chart of A... |
| GL_COA_TREE_VERSIONS_AGGR_DTLS | TABLE | 13 | GL_COA_TREE_VERSIONS_AGGR_DTLS contains account hierarchy versions that are published to balances cu... |
| GL_CODE_COMBINATIONS | TABLE | 110 | GL_CODE_COMBINATIONS contains valid account combinations for each accounting flexfield structure wit... |
| GL_CONCURRENCY_CONTROL | TABLE | 9 | GL_CONCURRENCY_CONTROL is used internally by Oracle General Ledger programs to prevent deadlock situ... |
| GL_CONCURRENT_SCHEDULES | TABLE | 12 | GL_CONCURRENT_SCHEDULES contains the definitions of schedules created by users. |
| GL_CROSS_RATE_RULE_DTLS | TABLE | 11 | GL_CROSS_RATE_RULE_DTLS notified the cross rates rule details including the conversion type, from cu... |
| GL_CROSS_RATE_TEMP | TABLE | 10 | This table is used for internal processing only |
| GL_DAILY_BALANCES | TABLE | 169 | GL_DAILY_BALANCES stores daily aggregate balances for detail and summary balance sheet accounts in s... |
| GL_DAILY_CONVERSION_TYPES | TABLE | 22 | GL_DAILY_CONVERSION_TYPES contains daily conversion rate types and their descriptions. This table co... |
| GL_DAILY_POST_INT1 | TABLE | 19 | This table is used for internal processing only |
| GL_DAILY_POST_INT2 | TABLE | 6 | This table is used for internal processing only |
| GL_DAILY_RATES | TABLE | 14 | GL_DAILY_RATES contains the daily conversion rates for foreign currency transactions. It replaces th... |
| GL_DATE_PERIOD_MAP | TABLE | 11 | GL_DATE_PERIOD_MAP stores the correlation between dates and non-adjusting periods for each accountin... |
| GL_DOC_SEQUENCE_AUDIT | TABLE | 9 | GL_DOC_SEQUENCE_AUDIT contains all the sequence values created for document sequences that are assig... |
| GL_ENCUMBRANCE_TYPES_B | TABLE | 12 | GL_ENCUMBRANCE_TYPES_B stores information about encumbrance types, including their IDs and descripti... |
| GL_ENCUMBRANCE_TYPES_TL | TABLE | 14 | GL_ENCUMBRANCE_TYPES_TL stores encumbrance type name in installed languages. Each row includes the e... |
| GL_ENC_CARRY_FORWARD_ACCTS | TABLE | 99 | GL_ENC_CARRY_FORWARD_ACCTS contains the accounts to be processed for a General Ledger encumbrance ba... |
| GL_ENC_CARRY_FORWARD_RULES | TABLE | 10 | GL_ENC_CARRY_FORWARD_RULES contains the General Ledger encumbrance balances carry forward rule defin... |
| GL_ESSBASE_BALANCES_DELTA | TABLE | 53 | This table contains sets of incremental balances that need to be applied to an Oracle Essbase cube. |
| GL_ESSBASE_BALANCES_TRACKING | TABLE | 15 | This table keeps track of the incremental data that needs to be published to an Oracle Essbase cube. |
| GL_ESSBASE_BAL_ROWS | TABLE | 2 | GL_ESSBASE_BAL_ROWS contains the transaction rows for a refresh balances run. |
| GL_ESSBASE_DAILY_BAL_DELTA | TABLE | 84 | This table contains sets of incremental average balances that need to be applied to an Oracle Essbas... |
| GL_ESSBASE_DUPLICATE_PARENTS | TABLE | 7 | GL_ESSBASE_DUPLICATE_PARENTS contains duplicate member information at parent level within the incomi... |
| GL_ESS_FILTER_SEGMENTS | TABLE | 10 | This table contains Accounting Flexfield segments for which partial flexfield artifacts are generate... |
| GL_FIXED_CONV_RATES | TABLE | 11 | GL_FIXED_CONV_RATES contains the fixed conversion rate between an old currency that is being phased ... |
| GL_FRC_REPORTS_B | TABLE | 16 | This table contains the list of reports available in BI catalog. This includes all the 3 types of re... |
| GL_FRC_REPORTS_TL | TABLE | 11 | This table contains the translated information about the BI reports. |
| GL_FRC_USER_ACCESS_REPORTS | TABLE | 18 | This table contains the list of reports from BI catalog that a user has access. This includes all th... |
| GL_FRC_USER_ACCESS_REPORT_TAGS | TABLE | 13 | This table contains the tags assigned to reports. |
| GL_FUN_INFOLET_CONFIGS | TABLE | 11 | This table contains infolet threshold data. |
| GL_FUSE_FR_FAVORITES | TABLE | 14 | This table stores the financial report meta data information along with the username and indicator t... |
| GL_HIERVIEW_LEDGER_INFO | TABLE | 11 | GL_HIERVIEW_LEDGER_INFO contains person info for a ledger and its image. |
| GL_HISTORICAL_RATES | TABLE | 19 | GL_HISTORICAL_RATES contains information about historical foreign currency translation rates. This t... |
| GL_IMPORT_REFERENCES | TABLE | 26 | GL_IMPORT_REFERENCES contains individual transactions from subledgers that have been summarized into... |
| GL_JE_ACTION_LOG | TABLE | 18 | GL_JE_ACTION_LOG stores the history of a journal batch. Each row represents an action that has occur... |
| GL_JE_BATCHES | TABLE | 44 | GL_JE_BATCHES contains journal entry batches. Each row includes the batch name, description, status,... |
| GL_JE_BSV_REPLICATION_RULES | TABLE | 10 | This table stores the primary balancing segment inclusion rules that are defined on the Map Primary ... |
| GL_JE_CATEGORIES_B | TABLE | 13 | GL_JE_CATEGORIES_B contains journal entry categories. Each journal entry in your Oracle Fusion Gener... |
| GL_JE_CATEGORIES_TL | TABLE | 14 | GL_JE_CATEGORIES_TL contains journal entry categories. Each row includes the category name and descr... |
| GL_JE_ERROR_CODES | TABLE | 20 | GL_JE_ERROR_CODES contains the error code of the journal lines. |
| GL_JE_HEADERS | TABLE | 72 | GL_JE_HEADERS contains journal entries. There is a one-to-many relationship between journal entry ba... |
| GL_JE_INCLUSION_RULES | TABLE | 14 | GL_JE_INCLUSION_RULES contains a set of journal sources and categories to be included/excluded for v... |
| GL_JE_LINES | TABLE | 64 | GL_JE_LINES contains the journal entry lines that you enter in the Enter Journals form. There is a o... |
| GL_JE_LINES_RECON | TABLE | 19 | GL_JE_LINES_RECON contains journal lines reconcilation information. |
| GL_JE_SEGMENT_VALUES | TABLE | 11 | GL_JE_SEGMENT_VALUES contains the balancing and management segment values used in each journal entry... |
| GL_JE_SOURCES_B | TABLE | 18 | GL_JE_SOURCES_B contains journal entry sources. Each journal entry in your Oracle General Ledger app... |
| GL_JE_SOURCES_TL | TABLE | 14 | GL_JE_SOURCES_TL contains source name in installed languages. Each row includes the user source name... |
| GL_JI_ERROR_CODES | TABLE | 14 | GL_JI_ERROR_CODES is populated with new row or rows if Journal Import process failed. Contents of th... |
| GL_LEDGERS | TABLE | 102 | GL_LEDGERS contains information about the ledgers defined in the Accounting Setup Manager and the le... |
| GL_LEDGER_CONFIGURATIONS | TABLE | 11 | GL_LEDGER_CONFIGURATIONS contains information about a primary ledger. The completion status code ind... |
| GL_LEDGER_CONFIG_DETAILS | TABLE | 15 | GL_LEDGER_CONFIG_DETAILS stores information about a primary ledger, its related secondary ledgers an... |
| GL_LEDGER_NORM_SEG_VALS | TABLE | 17 | GL_LEDGER_NORM_SEG_VALS contains information about the balancing segment values that are assigned to... |
| GL_LEDGER_RELATIONSHIPS | TABLE | 42 | GL_LEDGER_RELATIONSHIPS contains the relationships between ledgers. Each relationship between a prim... |
| GL_LEDGER_SEGMENT_VALUES | TABLE | 15 | GL_LEDGER_SEGMENT_VALUES contains information about the balancing segment values that are assigned t... |
| GL_LEDGER_SET_ASSIGNMENTS | TABLE | 11 | GL_LEDGER_SET_ASSIGNMENTS contains information about each ledger or ledger set that is contained wit... |
| GL_LEDGER_SET_NORM_ASSIGN | TABLE | 12 | GL_LEDGER_SET_NORM_ASSIGN contains information about each ledger or ledger set contained in a ledger... |
| GL_LEDGER_SET_REQUESTS | TABLE | 12 | GL_LEDGER_SET_REQUESTS stores information about all the child requests spawned by a parent request s... |
| GL_LEGAL_ENTITIES_BSVS | TABLE | 11 | GL_LEGAL_ENTITIES_BSVS stores balancing segment values assigned to a legal entity. |
| GL_LE_VALUE_SETS | TABLE | 8 | GL_LE_VALUE_SETS stores balancing segment value sets assigned to a legal entity. |
| GL_NET_INCOME_ACCOUNTS | TABLE | 15 | GL_NET_INCOME_ACCOUNTS contains the net income accounts for each balancing segment value of each led... |
| GL_PACS_COMBINATIONS | TABLE | 16 | This table contains the partial account combinations that are associated with a partial account comb... |
| GL_PACS_DEFINITIONS | TABLE | 18 | This table contains definitions of partial account combination sets. A partial account combination s... |
| GL_PERIODS | TABLE | 22 | GL_PERIODS contains information about the accounting periods that are defined using the Accounting C... |
| GL_PERIOD_PARTITIONS | TABLE | 18 | This table stores information about the partitioning of Oracle Fusion General Ledger tables by perio... |
| GL_PERIOD_SETS | TABLE | 11 | GL_PERIOD_SETS stores the calendars you define using the Accounting Calendar form. Each row includes... |
| GL_PERIOD_STATUSES | TABLE | 26 | GL_PERIOD_STATUSES contains the statuses of your accounting periods. Each row includes the accountin... |
| GL_PERIOD_TYPES | TABLE | 12 | GL_PERIOD_TYPES contains the period types you define using the Period Types form. Each row includes ... |
| GL_POSTING_INTERIM | TABLE | 65 | This is global temporary table. Posting and Open period programs uses this table. |
| GL_PURGE_DATA_TO_PURGE | TABLE | 21 | This table stores the details of what is going to be purged after the purge action for specific crit... |
| GL_PURGE_SETUP | TABLE | 15 | This table stores information about the archive and purge of data for each business object. It store... |
| GL_PURGE_SETUP_DETAILS | TABLE | 12 | This table stores the number of years to retain archived data, also known as the retention period, a... |
| GL_PURGE_TRACKING | TABLE | 23 | This table stores the archive and purge status for each business object and fiscal year. It stores t... |
| GL_PURGE_TRACKING_DETAILS | TABLE | 17 | This table stores the purge status of a business object, ledger, or legal entity. It is used only wh... |
| GL_PURGE_TRACKING_ERRORS | TABLE | 18 | This table stores any validation errors that are preventing a business object and fiscal year from b... |
| GL_PURGE_TRACKING_HISTORY | TABLE | 15 | This table stores the archive and purge related Enterprise Service Scheduler requests launched for a... |
| GL_RECONCILIATION_RULES | TABLE | 18 | This table contains the reconciliation types that represent reconcilable clearing accounts and the a... |
| GL_REPLICATION_JOURNALS | TABLE | 23 | This table stores posted journal batch and header information from a source primary ledger when prim... |
| GL_REQUEST_INFORMATION | TABLE | 18 | This table contains request information for General Ledger scheduled processes that is used to deter... |
| GL_REVALUATIONS | TABLE | 23 | GL_REVALUATIONS contains the Revaluation definitions. Each row includes a revaluation's identifier, ... |
| GL_REVAL_ACCOUNT_RANGES | TABLE | 101 | GL_REVAL_ACCOUNT_RANGES contains the account ranges to be processed for a revaluation. Each row incl... |
| GL_REVAL_FX_POSITION_ACCOUNTS | TABLE | 16 | GL_REVAL_FX_POSITION_ACCOUNTS contains the FX Revaluation Setup for Balance Sheet FX Position Accoun... |
| GL_ROW_MULTIPLIERS | TABLE | 10 | GL_ROW_MULTIPLIERS contains information necessary to expand the period information from GL_PERIODS i... |
| GL_SEGMENT_FREQUENCIES | TABLE | 10 | GL_SEGMENT_FREQUENCIES stores statistical information about the data in the GL_CODE_COMBINATIONS and... |
| GL_SEGVAL_INHERIT_HISTORY | TABLE | 12 | GL_SEGVAL_INHERIT_HISTORY keeps track of the segment value attribute maintenance records for each ch... |
| GL_SEG_VAL_HIERARCHIES | TABLE | 13 | GL_SEG_VAL_HIERARCHIES contains the relationship between various nodes in a given tree version in ro... |
| GL_SEG_VAL_HIER_CF | TABLE | 235 | GL_SEG_VAL_HIER_CF uses the structure of the FND_TREE_NODE_CF table as a template. It holds the rela... |
| GL_SEG_VAL_HIER_RF | TABLE | 28 | GL_SEG_VAL_HIER_RF contains the relationship between various nodes in a given tree version in row-fl... |
| GL_STAT_ACCOUNT_UOM | TABLE | 10 | GL_STAT_ACCOUNT_UOM contains the units of measure that you enter in the statistical units of measure... |
| GL_STORAGE_PARAMETERS | TABLE | 18 | GL_STORAGE_PARAMETERS contains default storage parameters for interim tables in Oracle Fusion Genera... |
| GL_SUSPENSE_ACCOUNTS | TABLE | 11 | GL_SUSPENSE_ACCOUNTS contains the additional suspense accounts you have specified for each source an... |
| GL_SVSBF_USAGES | TABLE | 14 | This table contains information about which business functions are enabled for enforcement of segmen... |
| GL_SYSTEM_USAGES | TABLE | 14 | GL_SYSTEM_USAGES indicates whether a particular feature is being used by any user of the system. Cur... |
| GL_TFR_FX_POSITION_ACCOUNTS | TABLE | 12 | GL_TFR_FX_POSITION_ACCOUNTS contains the Transfer Setup for Income Statement Accounts. Each row incl... |
| GL_TRACK_DELTA_BALANCES | TABLE | 13 | GL_TRACK_DELTA_BALANCES contains information about requests to track incremental balances using the ... |
| GL_TRANSACTION_CALENDAR | TABLE | 17 | GL_TRANSACTION_CALENDAR contains the transaction calendars you define using the Transaction Calendar... |
| GL_TRANSACTION_DATES | TABLE | 10 | GL_TRANSACTION_DATES contains business day information users define using the Transaction Calendar f... |
| GL_TRANSLATION_INTERIM | TABLE | 56 | This column is used in internal processing only |
| GL_TRANSLATION_STATUSES | TABLE | 19 | This column is used in internal processing only |
| GL_TRANSLATION_TRACKING | TABLE | 20 | GL_TRANSLATION_TRACKING contains information about foreign currency translation history. Each row st... |
| GL_USSGL_ACCOUNT_PAIRS | TABLE | 10 | GL_USSGL_ACCOUNT_PAIRS has the budgetary account pairs that are automatically debited and credited w... |
| GL_USSGL_TRANSACTION_CODES | TABLE | 13 | GL_USSGL_TRANSACTION_CODES contains user defined codes that tell Oracle General Ledger how to genera... |
| GL_XFR_HISTORY | TABLE | 17 | GL_XFR_HISTORY contains Oracle E-Business Suite to Oracle Fusion Cloud coexistence transfer run hist... |
| GL_XFR_HISTORY_FILES | TABLE | 12 | GL_XFR_HISTORY_FILES contains the setup and balances data files for Oracle E-Business Suite to Oracl... |
| GL_XFR_LEDGER_BSV_MAPS | TABLE | 10 | GL_XFR_LEDGER_BSV_MAPS contains the mapping information on balance transfer run balancing segment va... |
| GL_XFR_SOURCE_SYSTEMS | TABLE | 15 | GL_XFR_SOURCE_SYSTEMS contains the enterprise source system information. |
| GL_XFR_SYSTEM_LEDGERS | TABLE | 10 | GL_XFR_SYSTEM_LEDGERS contains the mapping between legacy and Oracle Fusion ledgers. |
| GL_XFR_TRACKING | TABLE | 13 | GL_XFR_TRACKING contains details about balance transfer run status. |
| GL_XLATE_POSTING_INTERIM | TABLE | 63 | This column is used in internal processing only |
| HR_ALL_ORGANIZATION_UNITS_F | TABLE | 21 | This is the master table which holds all the organization IDs. |
| HR_ALL_POSITIONS_F | TABLE | 58 | Positions main table storing all position attributes |
| HR_ALL_POSITIONS_F_TL | TABLE | 13 | Positions table storing translatable position attributes |
| HR_API_HOOKS | TABLE | 17 | This table contains data sourced from HR core development, legislation development teams and legisla... |
| HR_API_HOOK_CALLS | TABLE | 22 | Lists which extra logic, package procedures or formula, should be called from the API hook points. T... |
| HR_API_MODULES | TABLE | 14 | This table contains details of the business processes and row handlers which contain user hooks. Thi... |
| HR_API_USER_HOOK_REPORTS | TABLE | 3 | When the API user hook pre-processor program is being executed this table will contain data. It is u... |
| HR_DOCUMENTS_OF_RECORD | TABLE | 193 | This table contains information about the legislative or employment related documents of a person. |
| HR_DOCUMENTS_OF_RECORD_ARCHIVE | TABLE | 193 | This table contains information about the archived data for document records. |
| HR_DOCUMENT_DELIVERY_PREFS | TABLE | 31 | HCM Reporting document delivery preferences |
| HR_DOCUMENT_TYPES_B | TABLE | 124 | This table will contain definitions for type of personal document that can be maintained by Document... |
| HR_DOCUMENT_TYPES_TL | TABLE | 24 | Translated Document Types for Documents of Record. |
| HR_DOR_MASS_REQUESTS | TABLE | 19 | This table contains information about the mass requests of the document records. |
| HR_DOR_MASS_REQUEST_LINES | TABLE | 14 | This table contains information about the mass request's lines. |
| HR_DOR_MASS_REQUEST_PARAMS | TABLE | 10 | This table contains information about the mass request's parameters . |
| HR_GENERATIVE_AI_PROMPTS | TABLE | 16 | This table stores the prompts customizations. |
| HR_GEN_AI_AGENTS | TABLE | 14 | This table stores the Gen AI Agents |
| HR_GEN_AI_AGENTS_B | TABLE | 30 | This table stores the Gen AI Agents |
| HR_GEN_AI_AGENTS_TL | TABLE | 14 | This table stores the seeded Gen AI Agents name and description. |
| HR_GEN_AI_AGENT_TOOLS | TABLE | 11 | This table stores the Gen AI Agent Tools |
| HR_GEN_AI_AGENT_TOOL_MAPPINGS | TABLE | 12 | This table stores the relationships between Agents and Tools. |
| HR_GEN_AI_DOCUMENTS | TABLE | 16 | This table stores the Gen AI Documents |
| HR_GEN_AI_DOCUMENTS_B | TABLE | 16 | This table stores the Gen AI Documents |
| HR_GEN_AI_DOCUMENTS_TL | TABLE | 11 | This table stores the Gen AI Documents name and description. |
| HR_GEN_AI_PROMPTS_SEED_B | TABLE | 28 | This table stores the seeded prompts. |
| HR_GEN_AI_PROMPTS_SEED_TL | TABLE | 15 | This table stores the seeded prompts label and description. |
| HR_GEN_AI_TOOLS | TABLE | 13 | This table stores the Gen AI Tools |
| HR_GEN_AI_TOOLS_B | TABLE | 28 | This table stores the Gen AI Tools |
| HR_GEN_AI_TOOLS_TL | TABLE | 15 | This table stores the seeded Gen AI Tools name and description. |
| HR_NAME_FORMATS | TABLE | 17 | This table stores the setup data defining name formats, which are the rules for constructing various... |
| HR_ORGANIZATION_INFORMATION_F | TABLE | 81 | This table holds the information types data for organizations. |
| HR_ORGANIZATION_INFORMATIO_EFC | TABLE | 13 | This table only contains a subset of the columns from the base table. Contains a copy of the NCU (Na... |
| HR_ORGANIZATION_UNITS_F_TL | TABLE | 15 | This table stores the translatable data for HR_ALL_ORGANIZATION_UNITS_F. |
| HR_ORG_CLASSIFICATIONS | TABLE | 48 | This table holds all the seeded classifications for organizations across FUSION. |
| HR_ORG_CLASSIFICATIONS_TL | TABLE | 15 | This table holds the translations for all the classifications. |
| HR_ORG_INFORMATION_TYPES | TABLE | 16 | This table holds all the 'Information Types' for all organization classifications. |
| HR_ORG_INFORMATION_TYPES_TL | TABLE | 15 | HR_ORG_INFORMATION_TYPES_TL holds translatable information from HR_ORG_INFORMATION_TYPES |
| HR_ORG_INFO_TYPES_BY_CLASS | TABLE | 14 | HR_ORG_INFO_TYPES_BY_CLASS is an intersection table between HR_ORG_INFORMATION_TYPES and HR_ORGANIZA... |
| HR_ORG_UNIT_CLASSIFICATIONS_F | TABLE | 19 | This holds the classification IDs for a given organization ID. |
| HR_SEARCH_VIEWS | TABLE | 21 | This table stores the Search Configuration views |
| HR_SEARCH_VIEW_ATTRIBUTES | TABLE | 27 | This table stores the search view attributes |
| HR_VBCS_ADV_SAVED_SEARCH | TABLE | 16 | Table that stores the Saved Searches definition for different HCM modules |
| HR_VBCS_LISTS | TABLE | 16 | HCM lists that store the criteria used to generate population of objects |
| HZ_ACCOUNT_HEALTH | TABLE | 16 | The HZ_ACCOUNT_HEALTH shows account health information from USM |
| HZ_ACCOUNT_ROLLUPS | TABLE | 121 | The HZ_ACCOUNT_ROLLUPS table stores information Rollup Metrics data. |
| HZ_ACCT_PRODUCT_RELATIONS | TABLE | 26 | The HZ_ACCT_PRODUCT_RELATIONS shows account product information from USM |
| HZ_ACCT_PROD_SUGGESTIONS | TABLE | 17 | The HZ_ACCT_PROD_SUGGESTIONS shows account product suggestions from USM |
| HZ_ADDRESS_USAGES | TABLE | 11 | The HZ_ADDRESS_USAGES table stores the address usages per country and address style. Address usages ... |
| HZ_ADDRESS_USAGE_DTLS | TABLE | 10 | The HZ_ADDRESS_USAGE_DTLS table stores the required geography components for addresses usages per co... |
| HZ_ADDTNL_PARTY_IDS | TABLE | 28 | The HZ_ADDTNL_PARTY_IDS table is used to capture all additional identifiers associated to a Party. F... |
| HZ_ADDTNL_PARTY_NAMES | TABLE | 34 | HZ_ADDTNL_PARTY_NAMES is used to capture all additional names/aliases, associated to a party. For ex... |
| HZ_CERTIFICATIONS | TABLE | 23 | The HZ_CERTIFICATIONS table stores information about accreditation that is awarded to a company by a... |
| HZ_CITIZENSHIP | TABLE | 25 | The HZ_CITIZENSHIP table stores information about a person's nationality. Since a person can be a ci... |
| HZ_CLASS_CATEGORIES | TABLE | 16 | The HZ_CLASS_CATEGORIES table stores the various categories, either industrial classification standa... |
| HZ_CLASS_CATEGORY_USES | TABLE | 14 | The HZ_CLASS_CATEGORY_USES table stores information on the classification of party. A party can be c... |
| HZ_CODE_ASSIGNMENTS | TABLE | 38 | The HZ_CODE_ASSIGNMENTS table stores the classification codes associated with a party along with the... |
| HZ_CONSUMER_PROFILES | TABLE | 126 | The HZ_CONSUMER_PROFILES table stores personal information about a party of the 'Consumer' type. Spe... |
| HZ_CONSUMER_PROFILES_XM | TABLE | 20 | Custom 1:M child entity of consumers. For example details of buying history. |
| HZ_CONTACT_POINTS | TABLE | 66 | Electronic methods of communication with parties The HZ_CONTACT_POINTS table stores information abou... |
| HZ_CONTACT_PREFERENCES | TABLE | 34 | The HZ_CONTACT_PREFERENCES table stores information about contact preferences for parties or their a... |
| HZ_CONTACT_ROLLUPS | TABLE | 32 | The HZ_CONTACT_ROLLUPS table stores information Rollup Metrics data. |
| HZ_CREDIT_RATINGS | TABLE | 110 | The HZ_CREDIT_RATINGS table stores information about the creditworthiness of a party. A credit ratin... |
| HZ_CUSTOMER_PROFILES_F | TABLE | 104 | The HZ_CUSTOMER_PROFILES_F table stores information about characteristics of a customer, customer ac... |
| HZ_CUST_ACCOUNT_ROLES | TABLE | 25 | The HZ_CUST_ACCOUNT_ROLES table stores information about a role or function that a party performs in... |
| HZ_CUST_ACCT_RELATE_ALL | TABLE | 27 | The HZ_CUST_ACCT_RELATE_ALL table stores information about relationships between customer accounts. ... |
| HZ_CUST_PROFILE_AMTS_F | TABLE | 61 | The HZ_CUST_PROFILE_AMTS table stores information about the credit limits specified for a customer p... |
| HZ_CUST_PROFILE_CLASSES | TABLE | 90 | Standard credit profile classes |
| HZ_CUST_PROF_CLASS_AMTS | TABLE | 55 | Customer profile class amount limits for each currency |
| HZ_EDUCATION | TABLE | 25 | The HZ_EDUCATION table stores general information about the educational history of a party of the PE... |
| HZ_EMAIL_DOMAINS | TABLE | 19 | The HZ_EMAIL_DOMAINS table holds all the email(actual, unreversed) domains, transposed email domains... |
| HZ_EMPLOYMENT_HISTORY | TABLE | 38 | The HZ_EMPLOYMENT_HISTORY table stores information about the employment and military service history... |
| HZ_FINANCIAL_NUMBERS | TABLE | 24 | The HZ_FINANCIAL_NUMBERS table stores detailed financial information for the HZ_FINANCIALS_REPORTS t... |
| HZ_FINANCIAL_PROFILE | TABLE | 25 | The HZ_FINANCIAL_PROFILE table stores information about the financial accounts owned by a party. For... |
| HZ_FINANCIAL_REPORTS | TABLE | 40 | The HZ_FINANCIAL_REPORTS table stores information about the reports on the financial status of a par... |
| HZ_GEOGRAPHIES | TABLE | 54 | The HZ_GEOGRPHIES table stores data representing physical geographies. For example, this table would... |
| HZ_GEOGRAPHY_IDENTIFIERS | TABLE | 25 | HZ_GEOGRPHY_IDENTIFIERS stores multiple identifiers used to describe the same geography. The values ... |
| HZ_GEOGRAPHY_RANGES | TABLE | 20 | The table HZ_GEOGRAPHY_RANGES stores ranges associated with a given geography. For example, counties... |
| HZ_GEOGRAPHY_TYPES_B | TABLE | 18 | The table HZ_GEOGRPHY_TYPES_B stores Geography Type classification for geographies: both Master Refe... |
| HZ_GEOGRAPHY_TYPES_TL | TABLE | 13 | The HZ_GEOGRPHY_TYPES_TL stores Geography Types in translated languages. |
| HZ_GEOGRAPHY_VALIDATIONS | TABLE | 9 | The HZ_GEOGRAPHY_VALIDATIONS table stores the geography validation types and corresponding user sele... |
| HZ_GEO_HIERARCHY_CF | TABLE | 52 | The HZ_GEO_HIERARCHY_CF table contains geography hierarchies in ten level of column-flattened struct... |
| HZ_GEO_IDEN_PROV_DTLS | TABLE | 16 | HZ_GEO_IDEN_PROV_DTLS is a tracking table to track the geographies by multiple providers.The intent ... |
| HZ_GEO_NAME_REFERENCES | TABLE | 19 | The table HZ_GEO_NAME_REFERENCES stores the mapping between location elements and Master Reference g... |
| HZ_GEO_NAME_REFERENCE_LOG | TABLE | 19 | The HZ_GEO_NAME_REFERENCE_LOG table stores the mapping log between location elements and Master Refe... |
| HZ_GEO_STRUCTURE_LEVELS | TABLE | 22 | The table HZ_GEO_STRUCTURE_LEVELS stores the geographical hierarchical structures. For example, the ... |
| HZ_GEO_STRUCT_MAP | TABLE | 10 | The HZ_GEO_STRUCT_MAP table stores the map attributes for which a mapping of location components and... |
| HZ_GEO_STRUCT_MAP_DTL | TABLE | 13 | The HZ_GEO_STRUCT_MAP_DTL table stores the actual mapping of location component and geography type f... |
| HZ_GROUP_PROFILES | TABLE | 51 | HZ_GROUP_PROFILES table stores the additional information about a party of the Group type. For examp... |
| HZ_GROUP_PROFILES_XM | TABLE | 20 | Custom 1:M child entity of groups. For example specific profile information for a Household group ty... |
| HZ_HIERARCHY_NODES | TABLE | 24 | The HZ_HIERARCHY_NODES table contains denormalized data for hierarchical relationships. |
| HZ_LOCATION_LOCALES | TABLE | 31 | This table contains address components of a physical address captured in a specific language. This i... |
| HZ_LOCATION_PROFILES | TABLE | 42 | The HZ_LOCATION_PROFILES table stores information, including a history of any changes and address va... |
| HZ_MERGE_DICTIONARY | TABLE | 27 | The HZ_MERGE_DICTIONARY table stores information about the tables affected by a party merge. This ta... |
| HZ_MOBILE_PREFIXES | TABLE | 14 | The HZ_MOBILE_PREFIXES table stores the prefixes for mobile telephone numbers based on the country c... |
| HZ_NAME_AND_ID_TYPES_B | TABLE | 14 | The HZ_NAME_AND_ID_TYPES_B is used to store the types of an additional party name or an additional p... |
| HZ_NAME_AND_ID_TYPES_TL | TABLE | 14 | The HZ_NAME_AND_ID_TYPES_TL is used to capture the [arty type descriptions in multiple languages. Th... |
| HZ_ORGANIZATION_PROFILES | TABLE | 139 | The HZ_ORGANIZATION_PROFILES table stores information specific to an Organization. This table gets p... |
| HZ_ORGANIZATION_PROFILES_CS | TABLE | 11 | The profile staging table collects value change and source information for profile records being cre... |
| HZ_ORGANIZATION_PROFILES_CX | TABLE | 5 | The profile index table stores value change information for profile records in the history table. Th... |
| HZ_ORGANIZATION_PROFILES_XM | TABLE | 20 | Custom 1:M child entity of organizations. For example details of yearly revenue, profit/loss of an o... |
| HZ_ORGANIZATION_PROFILES_XME1 | TABLE | 23 | This table store the Account object's extension objects |
| HZ_ORG_CONTACTS | TABLE | 35 | The HZ_ORG_CONTACTS table stores information about the position of the contact for a party or party ... |
| HZ_ORG_CONTACTS_XM | TABLE | 20 | Custom 1:M child entity of contacts. For example specific profile information for sales account cont... |
| HZ_ORG_CONTACT_ROLES | TABLE | 23 | The HZ_ORG_CONTACT_ROLES table stores information about the role of the contact position that is spe... |
| HZ_ORIG_SYSTEMS_B | TABLE | 21 | The HZ_ORIG_SYSTEMS_B table stores information about source systems, Source systems are systems that... |
| HZ_ORIG_SYSTEMS_TL | TABLE | 14 | The HZ_ORIG_SYSTEMS_TL table provides multilingual support for source system information from the HZ... |
| HZ_ORIG_SYS_MAPPING | TABLE | 15 | The HZ_ORIG_SYS_MAPPING table stores the mapping among source systems and owner table names. Source ... |
| HZ_ORIG_SYS_REFERENCES | TABLE | 26 | The HZ_ORIG_SYSTEM_REFERENCES table stores the mapping between source system references and the owne... |
| HZ_PARTIES_CONTACT_SECURITY | TABLE | 13 | This table controls the visibility of a Contact for a Sales Account party. This contains all Contact... |
| HZ_PARTIES_PURGE | TABLE | 18 | hz_parties_purge table stores all filter parameters used by user while parties purge |
| HZ_PARTIES_PURGE_LOG | TABLE | 25 | This Table keeps log for Parties Purge ESS |
| HZ_PARTIES_PURGE_PARTYIDS | TABLE | 8 | This table keeps List of partyId's for both I and M status |
| HZ_PARTIES_PURGE_PREVIEW | TABLE | 8 | This table keeps List of partyId's for both I status |
| HZ_PARTY_CLASSIFICATION_DN | TABLE | 68 | The HZ_PARTY_CLASSIFICATION_DN is a column flattened denormalization table storing all ten primary c... |
| HZ_PARTY_HIERARCHY_DENORM | TABLE | 15 | Oracle internal use only. This table hz_party_hierarchy_denorm store snapshot information of custome... |
| HZ_PARTY_HIER_CF_DENORM | TABLE | 24 | Oracle internal use only. This table hz_party_hier_path_denorm store snapshot information of custome... |
| HZ_PARTY_HIER_PATH_DENORM | TABLE | 12 | Oracle internal use only. This table hz_party_hier_path_denorm store snapshot information of custome... |
| HZ_PARTY_HIER_VERSION_DENORM | TABLE | 11 | Oracle internal use only. This table hz_party_hier_version_denorm store snapshot information of cust... |
| HZ_PARTY_PREFERENCES | TABLE | 26 | The HZ_PARTY_PREFERENCES table stores information about the preference values provided by a party. E... |
| HZ_PARTY_SITES_XM | TABLE | 20 | Custom 1:M child entity of addresses. For example specific profile information for sell-to addresses... |
| HZ_PARTY_SITE_USES | TABLE | 23 | The HZ_PARTY_SITE_USES table stores information about how a party site is used. Party sites can have... |
| HZ_PARTY_USAGES_B | TABLE | 16 | The HZ_PARTY_USAGES_B table stores the definition of a party usage. For example, it stores informati... |
| HZ_PARTY_USAGES_TL | TABLE | 16 | Provides multilingual support for party usage definitions. |
| HZ_PARTY_USAGE_RULES | TABLE | 15 | Stores party usage rules. |
| HZ_PARTY_USG_ASSIGNMENTS | TABLE | 24 | Stores information about party usage assignments. |
| HZ_PARTY_USG_FR_B | TABLE | 14 | Stores information about Party Usage Folter Rule definitions, including the code of the Filter Rule. |
| HZ_PARTY_USG_FR_MEMBERS | TABLE | 14 | Stores information about the members of a Party Usage Filter Rule. Each member can either be an incl... |
| HZ_PARTY_USG_FR_SFT_XCLS | TABLE | 12 | Stores information about the soft exclusions for members of a Party Usage Filter Rule |
| HZ_PARTY_USG_FR_TL | TABLE | 14 | Provides multilinguial support for information Party Usage Filter Rule definitions |
| HZ_PARTY_USG_LKUP_CODES | TABLE | 12 | The table is used to map a party usage code to data use din TCA setup |
| HZ_PERSON_INTEREST | TABLE | 27 | The HZ_PERSON_INTEREST table stores information about a person's personal interests. For example, if... |
| HZ_PERSON_LANGUAGE | TABLE | 25 | The HZ_PERSON_LANGUAGE table stores information on the languages that a person speaks, reads or writ... |
| HZ_PERSON_PROFILES | TABLE | 104 | The HZ_PERSON_PROFILES table stores personal and family information about a party of the 'Person' ty... |
| HZ_PERSON_PROFILES_CS | TABLE | 11 | The profile staging table collects value change and source information for profile records being cre... |
| HZ_PERSON_PROFILES_CX | TABLE | 5 | The profile index table stores value change information for profile records in the history table. Th... |
| HZ_PERSON_PROFILES_XM | TABLE | 20 | Custom 1:M child entity of persons. For example details of buying history. |
| HZ_PHONE_AREA_CODES | TABLE | 16 | The HZ_PHONE_AREA_CODES table stores the telephone area codes used for a specific country. For examp... |
| HZ_PHONE_COUNTRY_CODES | TABLE | 19 | The HZ_PHONE_COUNTRY_CODES table stores country-specific trelephone prefix information. For example,... |
| HZ_PHONE_FORMATS | TABLE | 16 | The HZ_PHONE_FORMATS table stores information about the telephone number format used for a specific ... |
| HZ_REF_ENTITIES | TABLE | 21 | Extensibility Reference Entities |
| HZ_REF_ENTITIES_XMM | TABLE | 26 | Extensible many-to-many relationship table used to store custom intersection records. |
| HZ_RELATIONSHIPS | TABLE | 73 | The HZ_RELATIONSHIPS table stores information about relationships between two parties. The SUBJECT_I... |
| HZ_RELATIONSHIPS_XM | TABLE | 20 | Custom 1:M child entity of relationships. For example specific profile information for competitor re... |
| HZ_RELATIONSHIP_TYPES | TABLE | 23 | The HZ_RELATIONSHIP_TYPES table defines the business rules that are associated with a relationship t... |
| HZ_RELATIONSHIP_TYPES_TL | TABLE | 20 | Provides multilingual support for relationship types definitions. |
| HZ_ROLE_RESPONSIBILITY | TABLE | 21 | The HZ_ROLE_RESPONSIBILITY table stores the responsibilities of a party in relation to an account ro... |
| HZ_STYLES_B | TABLE | 11 | The HZ_STYLES_B table stores information for high-level classifications that identify a particular m... |
| HZ_STYLES_TL | TABLE | 14 | The HZ_STYLES_TL table stores style description in all the languages the translation is enabled for. |
| HZ_STYLE_FMT_LAYOUTS_B | TABLE | 28 | The HZ_STYLE_FMT_LAYOUTS_B table identifies which attributes appear in a particular style format, as... |
| HZ_STYLE_FMT_LAYOUTS_TL | TABLE | 13 | The HZ_STYLE_FMT_LAYOUTS_TL table stores translation information for the HZ_STYLE_FMT_LAYOUTS_B tabl... |
| HZ_STYLE_FMT_LOCALES | TABLE | 17 | The HZ_STYLE_FMT_LOCALES table stores the style formats associated to a location, along with the lan... |
| HZ_STYLE_FMT_VARIATIONS | TABLE | 17 | The HZ_STYLE_FMT_VARIATIONS table stores information about variations in style formats. A style form... |
| HZ_STYLE_FORMATS_B | TABLE | 12 | The HZ_STYLE_FORMATS_B table stores information for specific style formats that are valid for one or... |
| HZ_STYLE_FORMATS_TL | TABLE | 14 | The HZ_STYLES_FORMATS_TL table stores translation information for the HZ_STYLES_FORMATS_B table, for... |
| HZ_USER_CONTACTS | TABLE | 12 | This table is store the association between Resources and Contacts. The table supports the feature t... |
| HZ_USER_FAVORITE_PARTIES | TABLE | 10 | This table is store the association between Users and Parties. The table supports the feature that a... |
| HZ_WORK_CLASS | TABLE | 20 | The HZ_WORK_CLASS table stores custom-defined classification information about a person's job title ... |
| IBY_ACCOUNT_OWNERS | TABLE | 20 | IBY_ACCOUNT_OWNERS stores the joint account owners of a bank account. |
| IBY_ACCPPMTMTHD | TABLE | 12 | Stores the instrument types accepted by a Funds Capture Payee |
| IBY_ACCTTYPE | TABLE | 13 | IBY_ACCTTYPE contains a list of various account types supported. For example for bank account, the a... |
| IBY_ACCT_PMT_PROFILES_B | TABLE | 28 | IBY_ACCT_PMT_PROFILES stores account-related information that completes the specification of the han... |
| IBY_ACCT_PMT_PROFILES_TL | TABLE | 13 | IBY_ACCT_PMT_PROFILES stores account-related information that completes the specification of the han... |
| IBY_ACK_PROCESS_PROFILES | TABLE | 15 | Stores configurations for how bank acknowledgments are processed |
| IBY_ACK_READERS | TABLE | 13 | IBY_ ACK_READERS defines code points for parsing payment instruction acknowledgments. |
| IBY_ADVANCED_VALIDATIONS_B | TABLE | 14 | This table contains conditions to process advanced validations. |
| IBY_ADVANCED_VALIDATIONS_TL | TABLE | 10 | This table contains the translated column of advanced validation |
| IBY_APPLICABLE_PMT_MTHDS | TABLE | 17 | IBY_APPLICABLE_PMT_MTHDS stores the payment method applicability information for company policy-base... |
| IBY_APPLICABLE_PMT_PROFS | TABLE | 15 | IBY_APPLICABLE_PMT_PROFS maps payment methods to payment process profiles. Since administrators can ... |
| IBY_BANK_ACCT_OWNER_CHNG_HIST | TABLE | 31 | This table contains the history of external bank account ownership verification and other related up... |
| IBY_BATCHES_ALL | TABLE | 59 | IBY_BATCHES_ALL stores information about batch operations for credit card transactions. A terminal-b... |
| IBY_BEPINFO | TABLE | 42 | IBY_BEPKEYS stores information about the payment systems. |
| IBY_BEPKEYS | TABLE | 16 | IBY_BEPKEYS links internal payers to their payment system account values. Oracle Payments can only s... |
| IBY_BEP_ACCT_OPT_NAME_B | TABLE | 17 | IBY_BEP_ACCT_OPT_NAME stores payment system account configuration names. |
| IBY_BEP_ACCT_OPT_NAME_TL | TABLE | 14 | IBY_BEP_ACCT_OPT_NAME stores payment system account configuration names. |
| IBY_BEP_ACCT_OPT_VALS | TABLE | 14 | IBY_BEP_ACCT_OPT_VALS stores values for the parameters defined in IBY_BEP_ACCT_OPT_NAME for a given ... |
| IBY_CC_ISSUER_RANGES | TABLE | 13 | Table contains card ranges for various credit card issuers. Used to remove structure from a credit c... |
| IBY_CODE_MAP_FIELDS | TABLE | 16 | Stores the code mapping definition for a format field, such as the bank account type in bank stateme... |
| IBY_CODE_MAP_FLD_VALUES | TABLE | 13 | Stores the input/ output codes defined for a code map field |
| IBY_CODE_MAP_GROUPS_B | TABLE | 10 | Define code map group information |
| IBY_CODE_MAP_GROUPS_TL | TABLE | 14 | Code map groups translation table |
| IBY_CREDITCARD | TABLE | 63 | This table contains records of the credit card details of the customers entered manually or imported... |
| IBY_CREDITCARD_H | TABLE | 32 | Holds historical data for credit cards |
| IBY_CREDITCARD_ISSUERS_B | TABLE | 13 | Holds the list of accepted card brands |
| IBY_CREDITCARD_ISSUERS_TL | TABLE | 14 | Holds the list of accepted card brands |
| IBY_DEBIT_AUTHORIZATIONS_F | TABLE | 30 | This table is used to store Debit Authorization details. |
| IBY_DEFAULT_BEP | TABLE | 13 | IBY_DEFAULT_BEP stores information that will allow a payment system account and funds capture proces... |
| IBY_DIGITAL_PAYMENT_ACCOUNTS | TABLE | 43 | This table stores the information about digital or virtual payment accounts. |
| IBY_DOCS_PAYABLE_ALL | TABLE | 98 | IBY_DOCS_PAYABLE_ALL stores Oracle Payments' representation of source products' documents payable. A... |
| IBY_DOCUMENTS_PAYABLE_H | TABLE | 96 | IBY_DOCUMENTS_PAYABLE_H stores historical snapshots of documents payable. This table contains denorm... |
| IBY_DOCUMENT_LINES | TABLE | 18 | IBY_DOCUMENT_LINES stores Oracle Payments' representation of individual line items for documents pay... |
| IBY_DOCUMENT_LINES_H | TABLE | 21 | IBY_DOCUMENT_LINES_H stores historical snapshots of document line items. This table contains denorma... |
| IBY_ECAPP | TABLE | 13 | IBY_ECAPP stores information about Electronic Commerce Applications registered with iPayment. Oracle... |
| IBY_EXTERNAL_PAYEES_ALL | TABLE | 37 | IBY_EXTERNAL_PAYEES_ALL stores payment-related attributes for the funds disbursement payment process... |
| IBY_EXTERNAL_PAYERS_ALL | TABLE | 22 | Payment attributes of the customer |
| IBY_EXTRACTS_B | TABLE | 16 | IBY_EXTRACTS stores every extract definition supported by the extract generation engine. |
| IBY_EXTRACTS_TL | TABLE | 13 | IBY_EXTRACTS stores every extract definition supported by the extract generation engine. |
| IBY_EXT_BANK_ACCOUNTS | TABLE | 64 | IBY_EXT_BANK_ACCOUNTS defines the external bank account entity. This table should not be translated ... |
| IBY_EXT_BANK_ACCT_CHANGE_HIST | TABLE | 70 | This table contains the history of external bank account verification and other related updates. |
| IBY_EXT_PARTY_PMT_MTHDS | TABLE | 26 | IBY_EXT_PARTY_PMT_MTHDS stores payment method applicability driven by the preferences of the externa... |
| IBY_FC_SELECTED_TRXNS_ALL | TABLE | 147 | IBY_FC_SELECTED_TRXNS_ALL stores information about batch operations for credit card transactions. A ... |
| IBY_FILE_ACKS | TABLE | 17 | Stores bank acknowledgments for the payment files sent |
| IBY_FNDCPT_PAYEE_APPL | TABLE | 10 | IBY_FNDCPT_PAYEE_APPL is a mapping table between internal payees and operating units. One payee may ... |
| IBY_FNDCPT_PMT_CHNNLS_B | TABLE | 16 | IBY_FNDCPT_PMT_CHNNLS defines all payment methods for the funds capture flow. Payment methods are ca... |
| IBY_FNDCPT_PMT_CHNNLS_TL | TABLE | 14 | IBY_FNDCPT_PMT_CHNNLS defines all payment methods for the funds capture flow. Payment methods are ca... |
| IBY_FNDCPT_SYS_CC_PF_B | TABLE | 43 | IBY_FNDCPT_SYS_CC_PF stores payment system-defined attributes of the credit card funds capture proce... |
| IBY_FNDCPT_SYS_CC_PF_TL | TABLE | 14 | IBY_FNDCPT_SYS_CC_PF stores payment system-defined attributes of the credit card funds capture proce... |
| IBY_FNDCPT_SYS_DC_PF_B | TABLE | 44 | IBY_FNDCPT_SYS_DC_PF stores payment system-defined attributes of the bank account electronic funds t... |
| IBY_FNDCPT_SYS_DC_PF_TL | TABLE | 14 | IBY_FNDCPT_SYS_DC_PF stores payment system-defined attributes of the bank account electronic funds t... |
| IBY_FNDCPT_SYS_EFT_PF_B | TABLE | 52 | IBY_FNDCPT_SYS_EFT_PF stores payment system-defined attributes of the bank account electronic funds ... |
| IBY_FNDCPT_SYS_EFT_PF_TL | TABLE | 14 | IBY_FNDCPT_SYS_EFT_PF stores payment system-defined attributes of the bank account electronic funds ... |
| IBY_FNDCPT_TX_EXTENSIONS | TABLE | 31 | Payment attributes for a given funds capture transaction |
| IBY_FNDCPT_TX_OPERATIONS | TABLE | 8 | IBY_FNDCPT_TX_OPERATIONS stores associations between transaction extension entities and authorizatio... |
| IBY_FNDCPT_TX_XE_COPIES | TABLE | 8 | IBY_FNDCPT_TX_XE_COPIES stores the copy relationship between transaction extension entities. This re... |
| IBY_FNDCPT_USER_CC_PF_B | TABLE | 15 | IBY_FNDCPT_USER_CC_PF stores a complete credit card process profile defined for a single payment sys... |
| IBY_FNDCPT_USER_CC_PF_TL | TABLE | 10 | IBY_FNDCPT_USER_CC_PF stores a complete credit card process profile defined for a single payment sys... |
| IBY_FNDCPT_USER_DC_PF_B | TABLE | 15 | IBY_FNDCPT_USER_DC_PF stores a complete credit card process profile defined for a single payment sys... |
| IBY_FNDCPT_USER_DC_PF_TL | TABLE | 10 | IBY_FNDCPT_USER_DC_PF stores a complete credit card process profile defined for a single payment sys... |
| IBY_FNDCPT_USER_EFT_PF_B | TABLE | 18 | IBY_FNDCPT_USER_EFT_PF stores a complete credit card process profile defined for a single payment sy... |
| IBY_FNDCPT_USER_EFT_PF_TL | TABLE | 13 | IBY_FNDCPT_USER_EFT_PF stores a complete credit card process profile defined for a single payment sy... |
| IBY_FORMATS_B | TABLE | 24 | IBY_FORMATS stores payment file format information, including the name of the XDO template used to c... |
| IBY_FORMATS_TL | TABLE | 13 | IBY_FORMATS stores payment file format information, including the name of the XDO template used to c... |
| IBY_FORMAT_TYPES_B | TABLE | 21 | Stores all format types in Oracle Payments |
| IBY_FORMAT_TYPES_TL | TABLE | 14 | MLS table (TL table ) for Format types |
| IBY_GEN_DOCS_PAYABLE | TABLE | 79 | IBY_GEN_DOCS_PAYABLE serves as a template for source product tables or views from which Oracle Payab... |
| IBY_GEN_DOCUMENT_LINES | TABLE | 22 | IBY_GEN_DOCUMENT_LINES serves as a template for source product tables or views from which Oracle Pay... |
| IBY_HOOK_DOCS_IN_PMT_T | TABLE | 30 | This is a temporary table that is used to store documents payable associated with payments. |
| IBY_HOOK_PAYMENTS_T | TABLE | 29 | Temporary table that stores payments that are to be passed to external applications via call outs or... |
| IBY_IBAN_COUNTRY_STRUCTURE | TABLE | 31 | This table contains IBAN structure based on country. |
| IBY_INBOUND_FILE | TABLE | 31 | Stores files received from external payment systems such as payment acknowledgments or bank statemen... |
| IBY_INSTRHOLDER | TABLE | 13 | Oracle internal table and no longer used. |
| IBY_INSTRUCT_SOURCE_APPS | TABLE | 8 | IBY_INSTRUCT_SOURCE_APPS stores a list of source products that submitted documents to be paid in eac... |
| IBY_INSTR_CREATION_RULES | TABLE | 34 | IBY_INSTR_CREATION_RULES specifies how payments are grouped into payment instructions. Payment instr... |
| IBY_INSTR_CTL_TEMPLATES_B | TABLE | 17 | This table stores the information about the payment instrument control templates available for a pla... |
| IBY_INSTR_CTL_TEMPLATES_TL | TABLE | 14 | This table stores the information about the payment instrument control templates available for a pla... |
| IBY_INSTR_CTL_TEMPLT_APPL_MCC | TABLE | 14 | This table stores the information about merchant category codes applicable to a payment instrument c... |
| IBY_INSTR_CTL_TEMPLT_OPTS_B | TABLE | 18 | This table stores the information about available payment instrument control template options and cu... |
| IBY_INSTR_CTL_TEMPLT_OPTS_TL | TABLE | 13 | This table stores the information about available payment instrument control options and custom data... |
| IBY_INSTR_CTL_TEMPLT_OPT_VALS | TABLE | 15 | This table stores the information about payment instrument control template option values. |
| IBY_INTERMEDIARY_ACCTS | TABLE | 20 | IBY_INTERMEDIARY_ACCTS defines intermediary bank account information. |
| IBY_INTERNAL_PAYERS_ALL | TABLE | 25 | IBY_INTERNAL_PAYERS_ALL stores payment-related attributes for the funds disbursement payment process... |
| IBY_LOGICAL_PMT_GROUPS | TABLE | 19 | Group that contains payments that are logically grouped |
| IBY_PAYEE | TABLE | 32 | IBY_PAYEE stores a row for each payee, such as a biller, merchant, or store at this site. |
| IBY_PAYMENTS_ALL | TABLE | 234 | IBY_PAYMENTS_ALL stores information on payments. A payment is a single check or fund transfer transa... |
| IBY_PAYMENTS_H | TABLE | 134 | IBY_PAYMENTS_H table stores historical snapshots of payments. This table contains denormalized versi... |
| IBY_PAYMENT_CODES_B | TABLE | 16 | This table stores all payment code information including bank instruction codes, delivery channel co... |
| IBY_PAYMENT_CODES_TL | TABLE | 15 | This table stores translation information for IBY_PAYMENT_CODES_B table. |
| IBY_PAYMENT_METHODS_B | TABLE | 33 | IBY_PAYMENT_METHODS stores the payment methods that Oracle Payments supports. A payment method is a ... |
| IBY_PAYMENT_METHODS_TL | TABLE | 14 | IBY_PAYMENT_METHODS stores the payment methods that Oracle Payments supports. A payment method is a ... |
| IBY_PAYMENT_REFERENCES | TABLE | 8 | IBY_PAYMENT_REFERENCES stores the current payment reference number. Payment reference numbers are ou... |
| IBY_PAYMENT_RULES | TABLE | 11 | IBY_PAYMENT_RULES stores the header-level information for a payment method defaulting rule. A defaul... |
| IBY_PAYMENT_TRXN_RESPONSES | TABLE | 39 | This table stores information about bank or payment integrator transaction details, such as payment ... |
| IBY_PAY_INSTRUCTIONS_ALL | TABLE | 51 | IBY_PAY_INSTRUCTIONS_ALL stores information on payment instructions. A payment instruction is a set ... |
| IBY_PAY_INSTRUCTIONS_H | TABLE | 36 | IBY_PAY_INSTRUCTIONS_H stores historical snapshots of payment instructions. This table contains deno... |
| IBY_PAY_SERVICE_REQUESTS | TABLE | 26 | IBY_PAY_SERVICE_REQUESTS stores payment process requests from source products. A payment process req... |
| IBY_PCARD_BIN_RANGE | TABLE | 13 | IBY_PCARD_BIN_RANGE stores the BIN ranges for all valid purchase cards. |
| IBY_PMTMTHD_CONDITIONS | TABLE | 15 | IBY_PMTMTHD_CONDITIONS stores the conditions for payment methods. Each condition is comprised of a p... |
| IBY_PMTSCHEMES | TABLE | 13 | IBY_PMTSCHEMES stores a list of payment schemes that are supported by a payment system. |
| IBY_PMT_CREATION_RULES | TABLE | 24 | IBY_PMT_CREATION_RULES specifies how documents payable are grouped into payments. Creation rules are... |
| IBY_PMT_INSTR_USES_ALL | TABLE | 22 | Payment instruments assignments |
| IBY_PMT_LOGICAL_GRP_RULES | TABLE | 18 | Stores user defined grouping rules that are used in creating payments by grouping together payments. |
| IBY_PMT_MTHD_ATTRIB_APPL | TABLE | 14 | IBY_PMT_MTHD_ATTRIB_APPL stores payment channel or method attribute applicability settings. |
| IBY_PMT_SYS_FORMATS | TABLE | 15 | IBY_PMT_SYS_FORMATS links payment system to the payment formats they support. When a user creates a ... |
| IBY_PMT_SYS_TRANSMISSIONS | TABLE | 11 | IBY_BEP_TRANSMISSIONS links payment systems to the transmission protocols they support. When a user ... |
| IBY_PROCESS_CONC_REQUESTS | TABLE | 10 | Contains concurrent requests details. |
| IBY_PROCESS_FUNCTIONS | TABLE | 9 | List of all payment functions represented within any given payment process request. Populated by bui... |
| IBY_PROCESS_ORGS | TABLE | 11 | List of all business units represented within any given payment process request. Populated by build ... |
| IBY_REMIT_ADVICE_SETUP | TABLE | 18 | IBY_REMIT_ADVICE_SETUP stores information on creating and delivering remittance information, or remi... |
| IBY_RESULT_CODES | TABLE | 13 | This table stores the result codes |
| IBY_ROUTINGINFO | TABLE | 25 | IBY_ROUTINGINFO stores information that maps payment method to the payment system and funds capture ... |
| IBY_RULE_CONDITIONS | TABLE | 13 | IBY_RULE_CONDITIONS stores the detail-level information for a payment method defaulting rule. Each r... |
| IBY_SECURITY_SEGMENTS | TABLE | 15 | Holds encrypted data such as credit card, debit card and bank account numbers. It also holds encrypt... |
| IBY_SECURITY_UPG | TABLE | 14 | IBY_SECURITY_UPG contains security upgrade temporary data. |
| IBY_SETUP_EXTENSIBILITY | TABLE | 15 | This table stores the additional and extensible information about any payment setup entity. |
| IBY_STATUS_OVERRIDES | TABLE | 19 | Used to override acknowledgment status for payments. |
| IBY_SYS_PMT_PROFILES_B | TABLE | 61 | IBY_SYS_PMT_PROFILES stores seeded information that specifies the bulk of payment processing behavio... |
| IBY_SYS_PMT_PROFILES_TL | TABLE | 14 | IBY_SYS_PMT_PROFILES stores seeded information that specifies the bulk of payment processing behavio... |
| IBY_SYS_SECURITY_OPTIONS | TABLE | 41 | IBY_SYS_SECURITY_OPTIONS stores the system security options that are used for funds capture processi... |
| IBY_SYS_SECURITY_SUBKEYS | TABLE | 11 | IBY_SYS_SECURITY_SUBKEYS stores the security sub-keys used for data encryption. A sub-key is a rando... |
| IBY_TANGIBLE | TABLE | 20 | IBY_TANGIBLE stores information about the bills or orders. |
| IBY_TEMP_CREDITCARDS | TABLE | 36 | IBY_TEMP_CREDITCARDS is the interface table for credit card import |
| IBY_TEMP_EXT_BANK_ACCTS | TABLE | 78 | IBY_TEMP_EXT_BANK_ACCTS defines the temporary records for external bank accounts. |
| IBY_TEMP_EXT_PARTY_PMT_MTHDS | TABLE | 15 | IBY_TEMP_EXT_PARTY_PMT_MTHDS stores payment method applicability driven by the preference of a certa... |
| IBY_TEMP_EXT_PAYEES | TABLE | 42 | IBY_TEMP_EXT_PAYEES stores payment processing attributes for external payees. |
| IBY_TEMP_EXT_PAYERS | TABLE | 26 | IBY_TEMP_EXT_PAYERS is the interface table corresponding to IBY_EXTERNAL_PAYERS_ALL |
| IBY_TEMP_INTERMEDIARY_ACCTS | TABLE | 34 | IBY_TEMP_INTERMEDIARY_ACCTS is an interface table for intermediary bank account information. |
| IBY_TEMP_PMT_INSTR_USES | TABLE | 19 | IBY_TEMP_PMT_INSTR_USES links external payees and payers to their external payment instruments. |
| IBY_TRANSACTION_ACKS | TABLE | 28 | Stores bank acknowledgments for the transactions sent. |
| IBY_TRANSACTION_ERRORS | TABLE | 45 | IBY_TRANSACTION_ERRORS stores any errors encountered during payment processing validations. |
| IBY_TRANSMIT_CONFIGS_B | TABLE | 15 | IBY_TRANSMIT_CONFIGS defines a transmission channel with all parameters for the communication scheme... |
| IBY_TRANSMIT_CONFIGS_TL | TABLE | 13 | IBY_TRANSMIT_CONFIGS defines a transmission channel with all parameters for the communication scheme... |
| IBY_TRANSMIT_PARAMETERS_B | TABLE | 19 | IBY_TRANSMIT_PARAMETERS stores a transmission protocol's input parameters. For example, this table i... |
| IBY_TRANSMIT_PARAMETERS_TL | TABLE | 14 | IBY_TRANSMIT_PARAMETERS stores a transmission protocol's input parameters. For example, this table i... |
| IBY_TRANSMIT_PROTOCOLS_B | TABLE | 13 | IBY_TRANSMIT_PROTOCOLS specifies the transmission protocols used by various process profiles. This t... |
| IBY_TRANSMIT_PROTOCOLS_TL | TABLE | 13 | IBY_TRANSMIT_PROTOCOLS specifies the transmission protocols used by various process profiles. This t... |
| IBY_TRANSMIT_VALUES | TABLE | 16 | IBY_TRANSMIT_VALUES stores the values for the parameters defined in IBY_TRANSMIT_PARAMETERS for a gi... |
| IBY_TRXN_CORE | TABLE | 49 | IBY_BEPKEYS stores information about the payment systems. |
| IBY_TRXN_DOCUMENTS | TABLE | 22 | This table stores the information for the transaction documents. |
| IBY_TRXN_ERROR_TOKENS | TABLE | 10 | IBY_TRXN_ERROR_TOKENS stores the values that are used to fill out the tokens in transaction error me... |
| IBY_TRXN_EXTENSIBILITY | TABLE | 10 | IBY_TRXN_EXTENSIBILITY stores payment system transactional data, which cannot be accommodated in the... |
| IBY_TRXN_FI | TABLE | 13 | IBY_TRXN_FI contains the details of a payment request that are specific for systems that support bot... |
| IBY_TRXN_SUMMARIES_ALL | TABLE | 107 | IBY_TRXN_SUMMARIES_ALL stores information about each payment request. This table is used for both on... |
| IBY_TRXN_TYPES_B | TABLE | 13 | IBY_TRXN_TYPES stores the payment processing transaction types required by the dependent products fo... |
| IBY_TRXN_TYPES_TL | TABLE | 15 | IBY_TRXN_TYPES stores the payment processing transaction types required by the dependent products fo... |
| IBY_UPG_PPP_B | TABLE | 85 | The table is used during upgrade of payment process profile data. |
| IBY_UPG_PPP_TL | TABLE | 11 | The table is used during upgrade of payment process profile data. |
| IBY_USED_PAYMENT_DOCS | TABLE | 10 | IBY_USED_PAYMENT_DOCS tracks information about which payment documents have been used when printing ... |
| IBY_VALIDATION_PARAMS_B | TABLE | 13 | IBY_VALIDATION_PARAMS stores parameters for each validation. For example, one validation controls th... |
| IBY_VALIDATION_PARAMS_TL | TABLE | 14 | IBY_VALIDATION_PARAMS stores parameters for each validation. For example, one validation controls th... |
| IBY_VALIDATION_SETS_B | TABLE | 15 | IBY_VALIDATION_SETS stores links to payment validations. These validations must be performed before ... |
| IBY_VALIDATION_SETS_TL | TABLE | 13 | IBY_VALIDATION_SETS stores links to payment validations. These validations must be performed before ... |
| IBY_VALIDATION_VALUES | TABLE | 15 | IBY_VALIDATION_VALUES stores the values for each validation parameter. For example, one validation c... |
| IBY_VAL_ASSIGNMENTS | TABLE | 19 | IBY_VAL_ASSIGNMENTS links validation sets to the appropriate validation entity. Through this table, ... |
| IBY_VCARD_PROGRAMS_B | TABLE | 24 | This table stores the information about virtual card programs. |
| IBY_VCARD_PROGRAMS_TL | TABLE | 14 | This table stores the information about virtual card programs. |
| IBY_VCARD_PROGRAM_FCA_USES | TABLE | 14 | This table stores the information about funding card accounts added under a virtual card program. |
| IBY_XCC_EXTRACT | TABLE | 29 | Stores the information which is needed for budget control flow |
| IEX_ASSIGNMENTS | TABLE | 13 | Table stores backup collector information for use in displaying a collectors work to backup collecto... |
| IEX_BANKRUPTCIES | TABLE | 58 | Information stored for a customer identified as bankrupt. |
| IEX_BANKRUPTCIES_DISPOSITIONS | TABLE | 11 | Stores collection bankruptcy disposition history records. |
| IEX_CASE_FOLDERS | TABLE | 11 | IEX_CASE_FOLDERS contains a grouping of transactions. Grouped transactions have a limited number of ... |
| IEX_CASE_FOLDER_OBJECTS | TABLE | 10 | IEX_CASE_FOLDER_OBJECTS contain the actual transactions grouped for the case. Grouped transactions h... |
| IEX_CUSTOMER_MSG_DETAILS | TABLE | 20 | This table contains actionable transaction and customer level data derived from the intent of each i... |
| IEX_CUST_BANKRUPTCIES | TABLE | 9 | Stores collection bankruptcy descriptive fields information. |
| IEX_DELINQUENCIES_ALL | TABLE | 22 | Stores transaction data about customer delinquencies. |
| IEX_DELINQ_SUMMARIES_ALL | TABLE | 59 | Stores delinquency summary information of all delinquent customers, accounts or sites. |
| IEX_DEL_BUFFERS | TABLE | 20 | This table is used by the delinquency management program to identify delinquencies. |
| IEX_DEL_STATUSES | TABLE | 18 | Stores the mapping of score to delinquency status. |
| IEX_DUNNINGS | TABLE | 39 | Holds data on all dunning transactions sent by the system. |
| IEX_DUNNING_PLANS_B | TABLE | 25 | This table stores the header level information for dunning plans. |
| IEX_DUNNING_PLANS_TL | TABLE | 15 | Dunning plans translated table. |
| IEX_DUNNING_TRANSACTIONS | TABLE | 12 | Stores transaction details of dunnings. |
| IEX_DUN_CONF_DETAILS | TABLE | 19 | Stores dunning configuration details. |
| IEX_ESSBASE_BALANCES | TABLE | 41 | IEX_ESSBASE_BALANCES table stores information about the receivable transactions, receipts and adjust... |
| IEX_ESSBASE_BAL_TRANSFER | TABLE | 40 | This table stores all the aging bucket amount information and pre-calculated Essbase metrices value ... |
| IEX_METRIC_SUMMARIES_ALL | TABLE | 16 | This is an obsolete table and not in use. |
| IEX_OBJECT_FILTERS | TABLE | 20 | Limits the segment of customers a strategy is applied against. |
| IEX_PRD_APPL_XREF | TABLE | 17 | Stores applied payment information on promised invoices. |
| IEX_PROMISE_DETAILS | TABLE | 28 | Stores promise to pay information on delinquent invoices. |
| IEX_QUESTIONNAIRE_ITEMS | TABLE | 15 | Setup table for questionnaire administration. |
| IEX_SCORES | TABLE | 28 | Stores all the score definitions. |
| IEX_SCORE_COMPONENTS | TABLE | 19 | Stores details about what items make a score. |
| IEX_SCORE_COMP_DET | TABLE | 17 | Stores range and value details for components |
| IEX_SCORE_COMP_PARAMS | TABLE | 18 | Stores parameters to the scoring components. The parameters are in the form of name and value pairs. |
| IEX_SCORE_COMP_TYPES_B | TABLE | 18 | Scoring component types base table. |
| IEX_SCORE_COMP_TYPES_TL | TABLE | 16 | Scoring component types translated table. |
| IEX_SCORE_DATA_POINT_HISTORIES | TABLE | 16 | IEX_SCORE_DATA_POINT_HISTORIES contains information about the data point results of scoring formula ... |
| IEX_SCORE_HISTORIES | TABLE | 22 | Stores historical data about collection scores. |
| IEX_STRATEGIES | TABLE | 30 | Strategy methods detailed information. |
| IEX_STRATEGY_ASSIGNMENT_MATRIX | TABLE | 30 | IEX_STRATEGY_ASSIGNMENT_MATRIX contains setup information about segments of Oracle Collections. This... |
| IEX_STRATEGY_SEGMENTS | TABLE | 14 | This table contains the transaction segments that can be used to define strategy tasks for a collect... |
| IEX_STRATEGY_TEMPLATES_B | TABLE | 28 | Template details for a strategy. |
| IEX_STRATEGY_TEMPLATES_TL | TABLE | 12 | Translated template details for a strategy. |
| IEX_STRATEGY_TEMPLATE_GROUPS | TABLE | 33 | Strategy details grouped within a strategy method. |
| IEX_STRATEGY_USER_ITEMS | TABLE | 35 | Additional tasks added by a user to a strategy. |
| IEX_STRATEGY_WORK_ITEMS | TABLE | 43 | Actionable work generated by a web-service when a strategy task is created. |
| IEX_STRATEGY_WORK_SKILLS | TABLE | 14 | Identified users with the appropriate competency for a strategy task. |
| IEX_STRATEGY_WORK_TEMP_XREF | TABLE | 20 | Reference table to associate strategy to strategy task. |
| IEX_STRY_TEMP_WORK_ITEMS_B | TABLE | 42 | This table stores strategy task work items. |
| IEX_STRY_TEMP_WORK_ITEMS_TL | TABLE | 13 | Translated strategy task details. |
| JA_AU_EARNING_TRANSACTIONS | TABLE | 184 | This table contains FIC earning transaction information. |
| JA_AU_IC_INVOICES | TABLE | 29 | This table contains FIC invoices information. |
| JA_AU_IC_JOURNALS | TABLE | 61 | This table contains FIC journals information. |
| JA_AU_PAY_TRANSACTIONS | TABLE | 193 | This table contains FIC payments transaction information. |
| JA_CN_ACCOUNT_BALANCES | TABLE | 64 | This table contains the beginning balance, period net debit amount, period net credit amount, and en... |
| JA_CN_ACCOUNT_STRUCTURES | TABLE | 28 | This table contains a column 'CODE_COMBINATION_ID' to uniquely identify one valid combination of acc... |
| JA_CN_CFS_ASSIGN_SUPS | TABLE | 12 | This table contains information about cash flow statement, in or out flow, and the source. It stores... |
| JA_CN_EXPORT_OUTPUTS | TABLE | 11 | This table is used to store the outputs generated by financial data export for merge. |
| JA_CN_EXPORT_XML_TAGS | TABLE | 12 | This table contains tags in China for financial data export. |
| JA_CN_FD_DFF_ASSIGNMENTS | TABLE | 13 | This table contains context codes and column names for all descriptive flexfield used by programs of... |
| JA_CN_IMPORT_RPT | TABLE | 15 | This is the temporary table for vat invoice import. |
| JA_CN_JOURNALS_OF_PERIOD | TABLE | 16 | This table contains temporarily the journal lines that are not itemized by possible subsidiary of th... |
| JA_CN_JOURNAL_LINES | TABLE | 72 | This table contains accounting journal lines with information about related subsidiary accounts, if ... |
| JA_CN_JOURNAL_LINES_REQ | TABLE | 72 | This table contains temporarily the journal lines of the current session, which are itemized with in... |
| JA_CN_METHOD_ASSIGNMENTS | TABLE | 12 | This table contains information to indicate the depreciation for China National Audit Office version... |
| JA_CN_MISC_PARAM_ALL | TABLE | 18 | This table is used to store miscellaneous setup information for system options. |
| JA_CN_RULE_DFFS | TABLE | 13 | This table contains descriptive flexfield information for transfer rule. |
| JA_CN_RULE_HEADERS | TABLE | 13 | This table contains transfer rule header information for transfer rule. |
| JA_CN_RULE_TRX_TYPES | TABLE | 11 | This table contains transaction type information for transfer rule. |
| JA_CN_SUB_ACC_MAPPINGS | TABLE | 11 | This table contains information defined by 'Subsidiary Account Source'. This is the previous setting... |
| JA_CN_SUB_ACC_SOURCES | TABLE | 11 | This table contains subsidiary source information about project, third party and personnel, and the ... |
| JA_CN_SYSTEM_PARAMETERS | TABLE | 14 | This table contains information defined by 'System Options'. The 'Electronic Accounting Book Export'... |
| JA_CN_TRANSFER_RPT | TABLE | 16 | This table used for Transaction Transfer Output Report |
| JA_CN_TRANS_MAPPING | TABLE | 40 | This table is used to store journal and subledger transaction information. |
| JA_CN_TRXIMP_RPT | TABLE | 36 | This table is used to store temp data for VAT invoice import. |
| JA_CN_TRX_HEADERS_ALL | TABLE | 55 | This table contains transaction header information. |
| JA_CN_TRX_LINES_ALL | TABLE | 34 | This table contains Golden Tax transaction line information. |
| JA_CN_VAT_DFF_ASSIGNMENTS | TABLE | 12 | This table contains VAT descriptive flexfield assignments. |
| JA_CN_VAT_HEADERS_ALL | TABLE | 30 | This table contains VAT invoice header information. |
| JA_CN_VAT_LIMITS | TABLE | 12 | This table is used to store VAT limitation information for VAT invoice related setup. |
| JA_CN_VAT_LINES_ALL | TABLE | 26 | This table contains VAT invoice line information. |
| JA_CN_VAT_PARAM | TABLE | 9 | This table is used to store VAT invoice related setup header information for system options. |
| JA_CN_VAT_TAX_TYPES | TABLE | 9 | This table contains VAT tax type information for system options. |
| JA_CN_VOUCHER_NUMBERS | TABLE | 19 | This table contains the voucher numbers of the accounting journal lines. |
| JA_CN_VOUCHER_NUM_LEVELS | TABLE | 10 | Used for storing Voucher Number Generation Level setup information |
| JA_IN_EXPORT_LUT_DETAIL | TABLE | 11 | This table contains all detail letter of undertaking information for India export in the specific fi... |
| JA_IN_EXPORT_LUT_HEADER | TABLE | 12 | This table contains fiscal year setup information for India export under letter of undertaking. |
| JA_TH_AP_WHT_CERTIFICATES_ALL | TABLE | 27 | JA_TH_AP_WHT_CERTIFICATES_ALL contains all necessary information to issue withholding certificates. ... |
| JE_ES_MODELO_190_ALL | TABLE | 56 | Contains information relating to Spanish Withholding Tax processing. During each processing, records... |
| JE_FR_DAS2_DETAILS_T | TABLE | 71 | All data extracted from the core tables will be inserted into this table initially. |
| JE_FR_DAS2_ETB_HEADERS_T | TABLE | 41 | This table will be used to store the header information for an establishment. |
| JE_FR_DAS2_LE_ETB_SUMM_T | TABLE | 94 | This table will hold data from the JE_FR_DAS2_VEN_SUMMARY table as well as data summarized by the Le... |
| JE_FR_DAS2_LE_HEADERS_T | TABLE | 43 | This table will be used to store the header information for a Legal Entity. |
| JE_FR_DAS2_VEN_SUMMARY_T | TABLE | 71 | Five digits (from tenth position) of Tax Registration Number of Legal Entity and Legal Reporting Uni... |
| JE_GR_AR_AP_TRNOVR_ITF | TABLE | 31 | The JE_GR_AR_AP_TRNOVR_ITF table is no longer used by any current solution. |
| JE_GR_CUTOFF_RULES | TABLE | 13 | This setup table stores accounting cutoff rules for Greece. The accounting cutoff rules determine th... |
| JE_GR_JE_HEADER_SEQUENCE | TABLE | 9 | This table stores the Greek Accounting sequence and value for each journal entry whose journal categ... |
| JE_GR_TRNOVR_RULES | TABLE | 12 | JE_GR_TRNOVR_RULES contains exemption rule sets for Suppliers and Customers that are used by the Gre... |
| JE_GR_TRNOVR_RULE_LINES | TABLE | 12 | JE_GR_TRNOVR_RULE_LINES contains the detailed exemption clauses that identify which transactions wil... |
| JE_HU_BALANCES_REPORT | TABLE | 13 | JE_HU_BALANCES_REPORT contains information used for the Hungarian Asset Movement Schedule, the Hunga... |
| JE_IT_EXEMPT_LETTERS | TABLE | 20 | JE_IT_EXEMPT_LETTERS contains exemption letter information for suppliers. This table corresponds to ... |
| JE_IT_EXLET_SEQS | TABLE | 10 | JE_IT_EXLET_SEQS stores the sequence information for Italian exemption letters. |
| JE_IT_INVOICES_E_LISTING | TABLE | 20 | This table contains the electronic listing process information for invoices, that generates XML file... |
| JE_IT_TP_DECLARATION | TABLE | 20 | This table contains the third-party declaration process information that provides electronic reports... |
| JE_IT_YEAR_EX_LIMIT | TABLE | 15 | The JE_IT_YEAR_EX_LIMIT table stores yearly exemption limits and their monthly adjustments. |
| JE_NET_AGREEMENTS | TABLE | 37 | JE_NET_AGREEMENTS contains general information about netting agreements. |
| JE_NET_AP_INVS | TABLE | 23 | JE_NET_AP_INVS contains information about Payables invoices included in a netting batch. |
| JE_NET_AP_INV_TYPES | TABLE | 10 | JE_NET_AP_INV_TYPES contains information about the Payables invoice types that are included in a net... |
| JE_NET_AR_TRX_TYPES | TABLE | 11 | JE_NET_AR_TRX_TYPES contains information about the Receivables transaction types that are included i... |
| JE_NET_AR_TXNS | TABLE | 23 | JE_NET_AR_TXNS contains information about Receivables transactions included in a netting batch. |
| JE_NET_BATCHES | TABLE | 31 | JE_NET_BATCHES contains information about netting batches. |
| JE_NET_CUSTOMERS | TABLE | 12 | JE_NET_CUSTOMERS contains information about the customers that are included in a netting agreement. |
| JE_NET_INV_PAY_GROUPS | TABLE | 10 | JE_NET_INV_PAY_GROUPS contains information about Fusion Payables invoice pay groups, that are includ... |
| JE_NET_SUPPLIERS | TABLE | 12 | JE_NET_SUPPLIERS contains information about the suppliers that are included in a netting agreement. |
| JE_PCD_HISTORY | TABLE | 17 | The table stores the history of the Commercial Documents prints. |
| JE_PT_SAFT_ACCOUNTS | TABLE | 16 | JE_PT_SAFT_ACCOUNTS contains account balances and parent account details required to be used by SAFT... |
| JE_PT_SAFT_GL_DATA | TABLE | 33 | JE_PT_SAFT_GL_DATA contains the data required from Oracle Fusion Subledger Accounting and Oracle Fus... |
| JE_ZZ_VAT_REP_TRX_T | TABLE | 108 | Oracle internal use only. This temporary table contains reporting information related to tax, that m... |
| JG_DOC_SEQ_DERIVATIONS_ALL_F | TABLE | 27 | This table contains the information on the document sequence to be used for a given combination of c... |
| JG_ES_MODELO_DECL_LINES | TABLE | 32 | This table contains data used for the creation of Spanish Payables and Spanish Receivables Modelo 34... |
| JG_EXG_RATE_DIF | TABLE | 38 | JG_EXG_RATE_DIF contains records that are eligible to create invoice or journal and they will be pop... |
| JG_EXG_RATE_DIF_LINE | TABLE | 28 | JG_EXG_RATE_DIF_LINE contains line level details of records in JG_EXG_RATE_DIF table. |
| JG_FSCL_ATTRB_DEF_TMPL_F | TABLE | 17 | This table contains Fiscal Attribute Default Template values for Fiscal Document generation. |
| JG_FSCL_DOC_ASSET_CNTRLS_ALL_F | TABLE | 22 | This table contains setup details relating to fixed asset transfer information, that requires genera... |
| JG_FSCL_DOC_GEN_CNTRLS_ALL_F | TABLE | 27 | This table contains Fiscal Document generation controls and default values for Fiscal Document gener... |
| JG_FSCL_DOC_GEN_ERRORS_ALL | TABLE | 37 | This table contains errors found before sending the fiscal document to fiscal authority such as tax ... |
| JG_FSCL_DOC_GROUPS | TABLE | 14 | This table defines the Fiscal Document types that will be generated for a transaction that requires ... |
| JG_FSCL_DOC_HDRS_ALL | TABLE | 75 | This table contains transaction header level attributes required for generating fiscal document. Pro... |
| JG_FSCL_DOC_LEGAL_MSGS | TABLE | 10 | This table contains Fiscal Attribute Default Additional Legal Information for Fiscal Document genera... |
| JG_FSCL_DOC_LINES_ALL | TABLE | 213 | This table contains transaction line level attributes required for generating fiscal document. Produ... |
| JG_FSCL_DOC_LINE_DTLS_ALL | TABLE | 22 | This table contains transaction line details level attributes required for generating fiscal documen... |
| JG_FSCL_DOC_RELATIONS_ALL | TABLE | 61 | This table stores one or more fiscal documents details that are generated for one transaction in Fus... |
| JG_FSCL_DOC_SEQUENCES_F | TABLE | 14 | This table contains setup information for Fiscal Document Sequence number. |
| JG_FSCL_DOC_SERIES_B | TABLE | 11 | This table contains setup information for Fiscal Document Series. |
| JG_FSCL_DOC_SERIES_TL | TABLE | 10 | This table provides multilingual support (MLS) for each Fiscal Document Series. MLS enables you to s... |
| JG_FSCL_DOC_TIME_CONTROLS_F | TABLE | 14 | This table contains Fiscal Document Time controls for Tax Authority. |
| JG_FSCL_DOC_TYPES | TABLE | 9 | This table contains Fiscal Document Types definitions to be used by fiscal document processing of Re... |
| JG_FSCL_HDRS_ATRB_EXT_ALL | TABLE | 68 | This table contains additional transaction header level attributes required for generating fiscal do... |
| JG_FSCL_HDR_DTLS_ATRB_EXT_ALL | TABLE | 25 | This table contains multiple instances of records associated with the header of a transaction e.g. l... |
| JG_FSCL_IMPORT_ERRORS | TABLE | 26 | This table stores tax authority return information which could not be processed due to errors such a... |
| JG_FSCL_LINES_ATRB_EXT_ALL | TABLE | 39 | This table contains additional transaction line level attributes required for generating fiscal docu... |
| JG_FSCL_LN_DTLS_ATRB_EXT_ALL | TABLE | 20 | This table contains additional transaction line details level attributes required for generating fis... |
| JG_FSCL_TAX_LINES_ALL | TABLE | 73 | This table stores tax lines of the inbound fiscal document after validation. |
| JG_REPORTING_CONTEXT_T | TABLE | 35 | This temporary table contains the information of the data sections processed for the reporting conte... |
| JG_REPORTING_TRANSACTION_T | TABLE | 123 | This temporary table contains details of General Ledger, Accounts Payables, Accounts Receivable, Pay... |
| JG_SYSTEM_OPTIONS_ALL | TABLE | 10 | Stores information associated with regional localization system defaults and parameters defined for ... |
| JG_TAX_INVOICE_REFERENCES | TABLE | 41 | This table contains reference information related to the tax invoice that is obtained from the tax a... |
| JG_ZZ_AR_AP_TRNOVR_DECL_HDRS | TABLE | 19 | This table stores the turnover report extraction process parameter information which provides a hist... |
| JG_ZZ_AR_AP_TRNOVR_DECL_LINES | TABLE | 48 | This table stores information about reported transactions which are submitted to the Tax Authorities... |
| JG_ZZ_FA_REG_ITF | TABLE | 79 | JG_ZZ_FA_REG_ITF used by Fixed Assets Register Report |
| JG_ZZ_TA_ACCOUNT_RANGES | TABLE | 11 | This table stores the journal allocation natural account ranges. There is a one to many relationship... |
| JG_ZZ_TA_ALLOCATED_LINES | TABLE | 13 | This table stores the information on the original journal line used to allocate new journal line. Th... |
| JG_ZZ_TA_CC_RANGES | TABLE | 11 | This table stores the journal allocation cost center ranges. There is a one-to-many relationship bet... |
| JG_ZZ_TA_RULE_LINES | TABLE | 11 | This table stores the journal allocation lines. There is a one-to-many relationship between the jour... |
| JG_ZZ_TA_RULE_SETS | TABLE | 12 | This table stores the header information for each Journal Allocation Rule Set. This table correspond... |
| JG_ZZ_VAT_ALLOC_RULES | TABLE | 30 | For each source, financial and VAT transaction type captures allocation rules. These rules are used ... |
| JG_ZZ_VAT_BOX_ALLOCS | TABLE | 19 | Stores VAT box allocation information for tax and taxable amounts by period type. This information g... |
| JG_ZZ_VAT_BOX_ERRORS | TABLE | 9 | Stores the errors that are generated during VAT box allocation processing. These errors will be flus... |
| JG_ZZ_VAT_DOC_SEQUENCES | TABLE | 9 | Each record in this table stores the document sequence associated with the VAT register. For reporti... |
| JG_ZZ_VAT_FINAL_REPORTS | TABLE | 18 | This table captures data internally, by VAT reporting entity and period, when final print is process... |
| JG_ZZ_VAT_REGISTERS_B | TABLE | 11 | Base table that captures VAT Registers association with reporting entity configuration. For each rep... |
| JG_ZZ_VAT_REGISTERS_TL | TABLE | 10 | Captures translatable columns for table JG_ZZ_VAT_REGISTERS_B |
| JG_ZZ_VAT_REP_ENTITIES | TABLE | 35 | This is a key table which stores VAT reporting entities configuration setup. A combination of legal ... |
| JG_ZZ_VAT_REP_STATUS | TABLE | 38 | Stores the reporting status of the Tax Registration Number by period and source. |
| JG_ZZ_VAT_TRX_DETAILS | TABLE | 235 | JG_ZZ_VAT_TRX_DETAILS contains all payment related transactions selected for tax reporting. Taxable ... |
| JG_ZZ_WHT_RECONCILIATION | TABLE | 13 | This table contains summary of tax amount deposited with the government by the customer acting as th... |
| JG_ZZ_WHT_RECON_RECEIPTS | TABLE | 14 | This table contains receipts that are reconciled with withholding certificates periodically received... |
| JL_AR_AP_WHT_CERTIFICATES_ALL | TABLE | 31 | JL_AR_AP_AWT_CERTIFICATES_ALL contains all necessary information to issue withholding certificates. ... |
| JL_BR_AP_BANK_RETURNS_ALL | TABLE | 32 | Stores information associated with the payment request for the purchases made by a customer. |
| JL_BR_AP_COLLECTION_DOCS_ALL | TABLE | 60 | This table stores the details of Brazilian bank collection document records. |
| JL_BR_AP_COLLECT_EXT_ERRORS | TABLE | 10 | Stores information associated with the collection document to be imported. |
| JL_BR_AP_COLL_DOCS_DET_ALL | TABLE | 11 | This table stores the details of Brazilian bank detail collection document records. |
| JL_BR_AP_CONSOLID_INVOICES_ALL | TABLE | 24 | This table contains the consolidated invoice records for Brazil. |
| JL_BR_AP_OPERATIONS | TABLE | 11 | This table contains the operations fiscal codes for Brazil. |
| JL_BR_AR_BANK_INSTRUCTIONS | TABLE | 13 | This table stores the bank instruction codes. |
| JL_BR_AR_BANK_OCCURRENCES | TABLE | 15 | This table stores the mapping between bank occurrences and standard occurrences. |
| JL_BR_AR_BANK_RETURNS_ALL | TABLE | 48 | This table stores information on validated bank returns. |
| JL_BR_AR_BORDEROS_ALL | TABLE | 27 | This is an obsolete table and not in use. |
| JL_BR_AR_COLLECTION_DOCS_ALL | TABLE | 77 | This table stores the collection documents. |
| JL_BR_AR_COLL_BATCHES_ALL | TABLE | 34 | This table stores the collection remittance batches. |
| JL_BR_AR_COLL_DOCS_DET_ALL | TABLE | 21 | This table stores the details of the collection documents. |
| JL_BR_AR_COLL_DOCS_DET_WHT_ALL | TABLE | 22 | This table stores payment schedules requiring users to review and correct withholding amounts prior ... |
| JL_BR_AR_COMP_INV_ALL | TABLE | 41 | This table contains the complementary invoices. |
| JL_BR_AR_DISTRIBUTNS_ALL | TABLE | 31 | This is an obsolete table and not in use. |
| JL_BR_AR_MC_OCC_DOCS | TABLE | 10 | This table contains multiple reporting currency sub-table for JL_BR_AR_OCCURRENCE_DOCS_ALL. |
| JL_BR_AR_OCCURRENCE_DOCS_ALL | TABLE | 87 | This table contains occurrences for bank collection documents. |
| JL_BR_AR_PAY_SCHED_AUX | TABLE | 43 | This temporary table stores the bank transfer batches. |
| JL_BR_AR_POSTING_TMP | TABLE | 17 | This is an obsolete table and not in use. |
| JL_BR_AR_REC_MET_ACCTS_DTL_ALL | TABLE | 23 | This is an obsolete table and not in use. |
| JL_BR_AR_REC_MET_ACCTS_EXT_ALL | TABLE | 61 | This table stores the receipt method accounts. |
| JL_BR_AR_REMIT_BORDEROS_ALL | TABLE | 10 | This is an obsolete table and not in use. |
| JL_BR_AR_REMIT_COLL_BAT_ALL | TABLE | 10 | This table stores request identifiers for formatted bank transfers. |
| JL_BR_AR_SELECT_ACCOUNTS_ALL | TABLE | 27 | This table stores bank account distribution criteria for bank transfer batches. |
| JL_BR_AR_SELECT_CONTROLS_ALL | TABLE | 35 | This table stores the selection criteria for invoices sent to bank transfer batches. |
| JL_BR_CINFOS_BOOKS | TABLE | 13 | This is an obsolete table and not in use. |
| JL_BR_EILOG | TABLE | 11 | This table is an audit trial (log) table to keep track of the communication between partner software... |
| JL_BR_GL_LEGAL_REP | TABLE | 42 | This table contains the ledger book and subledger information. |
| JL_BR_INV_API_TRX_LINES_T | TABLE | 47 | This is a temporary table which is used internally by Oracle. |
| JL_BR_LOCAL_HOLIDAY_DATES | TABLE | 12 | This table contains the local holiday dates for Brazil. |
| JL_BR_LOCAL_HOLIDAY_SETS | TABLE | 14 | This table contains the local holiday sets for Brazil. |
| JL_BR_SPED_ACCT_CONFIGS_F | TABLE | 28 | This table contains the accounting configuration setup for legal entity and legal reporting unit. |
| JL_BR_SPED_EXTR_DATA_H | TABLE | 45 | This table contains the financial information that has already been reported to the government. Once... |
| JL_BR_SPED_EXTR_DATA_T | TABLE | 45 | This table contains the financial data for reporting. The data is from various setup, and GL and SLA... |
| JL_BR_SPED_EXTR_MSGS | TABLE | 12 | This is an obsolete table and not in use. |
| JL_BR_SPED_EXTR_PARAM | TABLE | 38 | This is an obsolete table and not in use. |
| JL_BR_SPED_EXTR_PARAMS | TABLE | 16 | This table contains information about the set of parameters used for SPED extraction. |
| JL_BR_SPED_LEGAL_STATUS_F | TABLE | 11 | This table contains the legal status information for legal entity and legal reporting unit. |
| JL_BR_SPED_PARTIC_CODES | TABLE | 29 | This is an obsolete table and not in use. |
| JL_BR_SPED_PARTIC_REL | TABLE | 12 | This is an obsolete table and not in use. |
| JL_BR_SPED_PRCPNT_CODES | TABLE | 18 | This table contains participant information. A participant is an organization related to the first p... |
| JL_BR_SPED_PRCPNT_REGTRNS | TABLE | 12 | This table contains participant registration information. |
| JL_BR_SPED_PRCPNT_RELATIONS_F | TABLE | 13 | This table contains participant relationships information. |
| JL_CL_AP_WHT_CERTIFICATES_ALL | TABLE | 24 | JL_CL_AP_WHT_CERTIFICATES_ALL contains all necessary information to issue withholding certificates. ... |
| JL_HDR_FISCAL_ATTRBS_EXT | TABLE | 32 | This table is an extension table to the receivables transactions table. |
| JL_LINES_FISCAL_ATTRBS_EXT | TABLE | 38 | This table is an extension table to the RA_CUSTOMER_TRX_LINES_ALL table. |
| JL_MX_JE_LINES_T | TABLE | 43 | This table contains all the information about the journals created for the period. |
| JL_MX_JE_LINE_DETAILS_T | TABLE | 49 | This table contains the data used to populate the subledger transcation and its payments details. |
| JL_ZZ_ACCOUNT_QUALIFIERS | TABLE | 12 | This table stores classifications for the general ledger account segment values that would be used f... |
| JV_ACCOUNTING_HEADERS | TABLE | 20 | This table contains accounting header information for transactions generated within Joint Venture Ma... |
| JV_ACCOUNT_FILTERS | TABLE | 12 | This table contains the account filters within an account filter set to be used by Joint Venture Man... |
| JV_ACCOUNT_FILTER_SETS_B | TABLE | 9 | This table contains the account filter sets within an account set to be used by Joint Venture Manage... |
| JV_ACCOUNT_FILTER_SETS_TL | TABLE | 11 | This table contains the translated account filter set descriptions. |
| JV_ACCOUNT_FILTER_VALUES | TABLE | 9 | This table contains the account filter values within an account filter to be used by Joint Venture M... |
| JV_ACCOUNT_SETS_B | TABLE | 21 | This table contains the account sets to be used by Joint Venture Management processes. |
| JV_ACCOUNT_SETS_TL | TABLE | 11 | This table contains the translated account set descriptions. |
| JV_ADJ_FACTOR_VALUES | TABLE | 11 | This table contains the adjustment factor values within a periodic adjustment factor to be used by J... |
| JV_ASSIGNMENT_RULES_B | TABLE | 18 | This table contains assignment rules for each joint venture. These rules are used to assign ownershi... |
| JV_ASSIGNMENT_RULES_TL | TABLE | 11 | This table contains translated assignment rule descriptions. |
| JV_CI_AGREEMENTS_B | TABLE | 14 | This table contains the carried interest agreements for each joint venture. |
| JV_CI_AGREEMENTS_TL | TABLE | 11 | This table contains translated carried interest agreement descriptions. |
| JV_CI_DISTRIBUTIONS | TABLE | 44 | This table contains the tracking distributions for carried interest agreements. |
| JV_CI_DISTRIBUTION_PENALTIES | TABLE | 21 | This table contains the penalty amounts for a carried interest distribution. |
| JV_CI_GROUPS_F_B | TABLE | 11 | This table contains the date effective stakeholder groups within the carried interest agreement. |
| JV_CI_GROUPS_TL | TABLE | 11 | This table contains translated carried interest agreement stakeholder group descriptions. |
| JV_CI_GROUP_LINES | TABLE | 13 | This table contains the consenting and non-consenting stakeholders in a carried interest agreement a... |
| JV_CI_PAYOUT_BALANCES | TABLE | 20 | This table contains the balances used to determine payout for consenting and nonconsenting stakehold... |
| JV_CI_PENALTIES_B | TABLE | 14 | This table contains the carried interest penalty definitions by joint venture, carried interest agre... |
| JV_CI_PENALTIES_TL | TABLE | 11 | This table contains translated carried interest penalty descriptions. |
| JV_CI_PENALTY_PERCENTAGES_B | TABLE | 14 | This table contains the carried interest penalty percentage line details such as category, name, acc... |
| JV_CI_PENALTY_PERCENTAGES_TL | TABLE | 10 | This table contains translated carried interest penalty percent names. |
| JV_CONTRIBUTIONS_B | TABLE | 32 | This table contains joint venture partner contribution definitions. |
| JV_CONTRIBUTIONS_TL | TABLE | 10 | This table contains translated joint venture partner contribution definition descriptions. |
| JV_CONTRIBUTION_REFERENCES | TABLE | 29 | This table contains transaction references that are associated with the partner contribution. |
| JV_CONTRIBUTION_REQUESTS_B | TABLE | 24 | This table contains joint venture partner contribution requests. These requests are used to create p... |
| JV_CONTRIBUTION_REQUESTS_TL | TABLE | 11 | This table contains the joint venture partner contribution requests translation definition. |
| JV_COST_CENTERS | TABLE | 9 | This table contains the primary segment values for each joint venture. These values are used to iden... |
| JV_DISTRIBUTABLE_PROJECTS | TABLE | 11 | This table contains distributable project, task, expenditure type values for each joint venture. The... |
| JV_DISTRIBUTABLE_VALUES | TABLE | 40 | This table contains values for each segment that represent accounts that are distributable. Only seg... |
| JV_DISTRIBUTIONS | TABLE | 56 | This table contains distribution records generated for each stakeholder from the processing of joint... |
| JV_EXCLUDED_SUBLEDGERS | TABLE | 9 | This table contains subledgers to exclude when running the process to identify joint venture transac... |
| JV_GENERATED_TRANSACTIONS | TABLE | 33 | This table contains the joint venture internally generated transactions such as overhead that do not... |
| JV_INVOICING_PARTNERS_B | TABLE | 17 | This table contains the associated customer and supplier information for invoicing partners. |
| JV_INVOICING_PARTNERS_TL | TABLE | 11 | This table contains the translated invoicing partner descriptions. |
| JV_JOINT_VENTURES_B | TABLE | 66 | This table contains the joint venture definitions. |
| JV_JOINT_VENTURES_TL | TABLE | 11 | This table contains the translated joint venture descriptions. |
| JV_MEASURE_TYPES_B | TABLE | 12 | This table contains the operational measure types that can be used for recording the operational mea... |
| JV_MEASURE_TYPES_TL | TABLE | 11 | This table contains the translated operational measure type descriptions. |
| JV_OPERATIONAL_MEASURES | TABLE | 17 | This table contains the operational measures for joint ventures. These measures are used to allocate... |
| JV_OPERATIONAL_STATES | TABLE | 13 | This table contains the operational activities which represent what is going on in a joint venture a... |
| JV_OVERHEAD_MEASURE_TYPES | TABLE | 9 | This table contains the operational measure types to be used by an overhead method. |
| JV_OVERHEAD_METHODS_F_B | TABLE | 37 | This table contains the date effective overhead methods for each joint venture. These methods are us... |
| JV_OVERHEAD_METHODS_TL | TABLE | 12 | This table contains the translated overhead method descriptions. |
| JV_OWNER_PERCENTS_F_B | TABLE | 18 | This table contains the date effective ownership percentage information for a joint venture. |
| JV_OWNER_PERCENTS_TL | TABLE | 11 | This table contains the translated ownership percentage descriptions. |
| JV_OWNER_PERCENT_LINES | TABLE | 12 | This table contains the stakeholders and their percentage of interest for a joint venture’s ownershi... |
| JV_PERIODIC_ADJ_FACTORS_B | TABLE | 9 | This table contains the periodic adjustment factors to be used by Joint Venture Management processes... |
| JV_PERIODIC_ADJ_FACTORS_TL | TABLE | 11 | This table contains the translated periodic adjustment factor descriptions. |
| JV_PROJECT_FILTERS | TABLE | 12 | This table contains the project filters within a project filter set to be used by Joint Venture Mana... |
| JV_PROJECT_FILTER_SETS_B | TABLE | 9 | This table contains the project filter sets within a project set to be used by Joint Venture Managem... |
| JV_PROJECT_FILTER_SETS_TL | TABLE | 11 | This table contains the translated project filter set descriptions. |
| JV_PROJECT_FILTER_VALUES | TABLE | 9 | This table contains the project filter values within a project filter to be used by Joint Venture Ma... |
| JV_PROJECT_SETS_B | TABLE | 11 | This table contains the project sets to be used by Joint Venture Management processes. |
| JV_PROJECT_SETS_TL | TABLE | 11 | This table contains the translated project set descriptions. |
| JV_PROJECT_VALUE_SETS | TABLE | 11 | This table contains project value sets to be used for an assignment rule to assign ownership definit... |
| JV_SLIDING_SCALE_THRESHOLDS | TABLE | 11 | This table contains the sliding scale thresholds to be used by an overhead method. |
| JV_STAKEHOLDERS_B | TABLE | 26 | This table contains the stakeholders associated with a joint venture. |
| JV_STAKEHOLDERS_TL | TABLE | 11 | This table contains the translated stakeholder descriptions. |
| JV_STAKEHOLDER_RPTG_BOOKS | TABLE | 11 | This table will contain ledger details for stakeholder reporting. |
| JV_SYSTEM_OPTIONS | TABLE | 30 | This table contains the joint venture system options. |
| JV_TRANSACTIONS | TABLE | 51 | This table will reference transactions that will be distributed among stakeholders of a joint ventur... |
| JV_TRANSACTION_CHANGES | TABLE | 34 | This table contains the history of changes made manually to joint venture transactions. |
| MO_GLOB_ORG_ACCESS_TMP | TABLE | 4 | MO_GLOB_ORG_ACCESS_TMP is used for processing of multi-org data. |
| PER_ABSENCE_ATTENDANCES | TABLE | 94 | This table holds details of employee absences from work. Records can be entered with PROJECTED dates... |
| PER_ABSENCE_ATTENDANCE_TYPES_B | TABLE | 88 | PER_ABSENCE_ATTENDANCE_TYPES holds user definitions of absence types. These types are used to identi... |
| PER_ABSENCE_CASES | TABLE | 84 | This table is to store the Details of Absence Cases. Absence Case is a collection of Absences of an ... |
| PER_ABS_ATTENDANCE_REASONS | TABLE | 11 | PER_ABS_ATTENDANCE_REASONS holds the list of absence reasons that may apply to an absence or attenda... |
| PER_ABS_ATTENDANCE_TYPES_TL | TABLE | 11 | PER_ABS_ATTENDANCE_TYPES_TL holds translated information for Absence Types. |
| PER_ACCRUAL_BANDS | TABLE | 15 | Length of service bands used in calculating accrual of paid time off. |
| PER_ACCRUAL_CALC_RULES | TABLE | 14 | Element entry values which contribute to the net value of Paid Time Off. |
| PER_ACCRUAL_PLANS_B | TABLE | 108 | The base table used to store PTO accrual plan definitions, (Paid time off). |
| PER_ACCRUAL_PLANS_TL | TABLE | 12 | Language dependent table . Stores the translated data for PER_ACCRUAL_PLANS_B |
| PER_ACL_EXCLUSIONS | TABLE | 10 | Stores exclusions for Oracle Search ACL computation. |
| PER_ACTIONS_B | TABLE | 174 | This table stores actions and has a foreign key of Action Types. Customers can add Actions for the g... |
| PER_ACTIONS_TL | TABLE | 15 | This table holds the translated ???short description??? of defined actions. |
| PER_ACTION_HEADERS_M | TABLE | 17 | MCPD supports Action Headers table |
| PER_ACTION_OCCURRENCES | TABLE | 30 | This table defines the action occurrences for an action. |
| PER_ACTION_REASONS_B | TABLE | 82 | This table stores all the action reasons for an action |
| PER_ACTION_REASONS_TL | TABLE | 15 | This table will store a list of action reasons for each action. This will also be translatable. |
| PER_ACTION_REASON_USAGES | TABLE | 88 | This is the intersection table to have many to many relationships between Actions and Action Reasons... |
| PER_ACTION_ROLE_MAPPING | TABLE | 11 | This table stores all the roles based on which an action need to be filtered |
| PER_ACTION_TYPES_B | TABLE | 18 | This tables stores Action Types. Action Types are the predefined business processes seeded by Oracle... |
| PER_ACTION_TYPES_TL | TABLE | 14 | Action types allows the grouping of the actions. This translatable table will store the list of acti... |
| PER_ACT_OCCURRENCE_EXTRA_INFO | TABLE | 108 | This table defines the extra information for action occurrences for an action |
| PER_ADDRESSES | TABLE | 73 | Address information for people. |
| PER_ADDRESSES_F | TABLE | 103 | This table holds addresses for a person or for a location. |
| PER_ALLOCATED_CHECKLISTS | TABLE | 115 | This table records the checklists allocated to a person. These may be copied from templates in PER_C... |
| PER_ALLOCATED_CHECKLISTS_TL | TABLE | 19 | PER_ALLOCATED_CHECKLISTS_TL : This is translation table for PER_ALLOCATED_CHECKLISTS |
| PER_ALLOCATED_TASKS | TABLE | 160 | This table records the tasks within an allocated checklist to a person. These may be copied from tem... |
| PER_ALLOCATED_TASKS_TL | TABLE | 26 | PER_ALLOCATED_TASKS_TL : This is translation table for PER_ALLOCATED_TASKS |
| PER_ALLOC_CHKLST_CONTACTS | TABLE | 16 | PER_ALLOC_CHKLST_CONTACTS : This table has contacts for allocated checklist. |
| PER_ALLOC_CHKLST_CONTENTS | TABLE | 13 | PER_ALLOC_CHKLST_CONTENTS : This table has contents of allocated checklist. |
| PER_ALLOC_TASK_COMMENTS | TABLE | 22 | PER_ALLOC_TASK_COMMENTS : Allocated Task Comments |
| PER_ALLOC_TASK_COM_CNDN_CRIT | TABLE | 24 | Table to store completion condition criteria for an allocated task |
| PER_ALLOC_TASK_COM_CONDNS_B | TABLE | 26 | Table to store completion conditions for an allocated task |
| PER_ALLOC_TASK_COM_CONDNS_TL | TABLE | 11 | Translation table of PER_ALLOC_TASK_COM_CONDNS_B |
| PER_ALLOC_TASK_NOTIFS | TABLE | 26 | PER_ALLOC_TASK_NOTIFS : This table has notifications for allocated task |
| PER_ALLOC_TASK_PERFORMERS | TABLE | 19 | Table to store performer details for an allocated task. |
| PER_ALLOC_TASK_STAGES | TABLE | 20 | This table is used to store the stages of a task in allocated checklist |
| PER_ALL_ASSIGNMENTS_M | TABLE | 301 | This stores two levels of the 3-Tier Model: Employment/Placement Terms (Level 2) and Assignments (Le... |
| PER_ALL_PEOPLE_F | TABLE | 19 | This table will store core personal data that is not expected to vary by Legislation Code, or has ne... |
| PER_AOR_ASG_DN | TABLE | 2 | This denormalized table holds the details of assignment which needs to be evaluated to calculate ass... |
| PER_AOR_AUTO_PROVISION | TABLE | 56 | This table holds AOR records processed by auto provision ESS job which will be committed to PER_ASG_... |
| PER_AOR_AUTO_PROV_HISTORY | TABLE | 55 | This table holds records from PER_ASG_RESPONSIBILITIES as history of records impacted by auto provis... |
| PER_AOR_REP_LOG | TABLE | 18 | This table holds log information of Refresh representatives ESS Job run which calculates the assignm... |
| PER_AOR_REP_STMTS | TABLE | 3 | This table holds the details of sql statements and these sqls will be used to calculate assignment r... |
| PER_AOR_RES_DN | TABLE | 57 | This denormalized table holds the details of scope attributes combination and person's areas of resp... |
| PER_AOR_TEMPLATE | TABLE | 19 | This table holds the basic information of a responsibility template |
| PER_AOR_TEMPLATE_CRITERIA | TABLE | 19 | Stores criteria associated to AoR Template Records. Records stored are Non-Date Effective records. |
| PER_AOR_TEMPLATE_DETAILS | TABLE | 26 | This table holds the element details of a responsibility template |
| PER_ASG_ABSENCE_RECORDING | TABLE | 15 | This table is stores the details of Absences recorded at the Assignment level. In case if an absence... |
| PER_ASG_ELIGIBLE_JOBS | TABLE | 27 | This table stores all the information about the eligible jobs that a worker has been authorized to w... |
| PER_ASG_PROPAGATE_UPDATES | TABLE | 33 | This custom staging and tracking table stores the execution status and metadata for attribute update... |
| PER_ASG_REPRESENTATIVES | TABLE | 16 | This is a de-normalized table which will hold mapping between worker & its representatives which are... |
| PER_ASG_RESPONSIBILITIES | TABLE | 56 | This table holds the details of a person's areas of responsibility, defined by reference to existing... |
| PER_ASG_SEC_MATRLZED_CACHE | TABLE | 4 | This table will hold materialized cache data for list of assignments a user has access to. |
| PER_ASSIGNMENT_DAY_ABSENCES | TABLE | 19 | The effect of an Absence on different Assignments can vary based on the Work Schedule assigned to th... |
| PER_ASSIGNMENT_EXTENSIONS_F | TABLE | 17 | To Store TaxReportingUnit Data which will be used to by ESS Job to fetch the the data from the Exten... |
| PER_ASSIGNMENT_EXTRA_INFO_M | TABLE | 148 | This stores extensible data (Customer, Localization or Verticalization) for Assignments or Sets of E... |
| PER_ASSIGNMENT_NOTES | TABLE | 14 | This stores notes related to each transaction performned. |
| PER_ASSIGNMENT_STATUS_TYPES | TABLE | 24 | This table holds pre-defined and user defined status types (for Assignments or Sets of Employment/Pl... |
| PER_ASSIGNMENT_STATUS_TYPES_TL | TABLE | 15 | This table holds the translated USER_STATUS definitions of statuses for a specific assignment or Set... |
| PER_ASSIGNMENT_SUPERVISORS_F | TABLE | 86 | This stores the supervisors associated to a particular assignment. This supports different relations... |
| PER_ASSIGN_GRADE_STEPS_F | TABLE | 86 | This table stores the step within a grade that an employee is currently on or is being paid at. This... |
| PER_ASSIGN_WORK_MEASURES_F | TABLE | 85 | This table holds information about the HR budget values for an assignment. An Assignment may be budg... |
| PER_BOOKINGS | TABLE | 10 | This table stores the booking details made for a person to attend an event or interview. |
| PER_BUSINESS_OBJECT_LIMIT | TABLE | 9 | Stores the limit for business object |
| PER_CALENDAR_EVENTS | TABLE | 19 | This table is used to hold calendar events like public holidays |
| PER_CALENDAR_EVENTS_TL | TABLE | 12 | Language dependent table . Stores the translated data for PER_CALENDAR_EVENTS |
| PER_CAL_EVENT_COVERAGE | TABLE | 14 | This table holds values used to determine the coverage of the calendar events to people on the syste... |
| PER_CHECKLISTS_B | TABLE | 117 | This table records the checklist templates. |
| PER_CHECKLISTS_TL | TABLE | 22 | PER_CHECKLISTS_TL holds translated information for Checklist Templates. |
| PER_CHECKLIST_ACTIONS | TABLE | 29 | PER_CHECKLIST_ACTIONS : Stores the event for a checklist |
| PER_CHECKLIST_ALERTS | TABLE | 17 | Table to store checklist and task alerts |
| PER_CHECKLIST_ALERT_CHUNKS | TABLE | 13 | Table to store checklist and task alert chunks |
| PER_CHECKLIST_ALERT_SETS | TABLE | 15 | Table to store checklist and task alert sets |
| PER_CHECKLIST_ALLOCATIONS | TABLE | 18 | Table to store allocation configuration which will be used for mass assigning journeys. |
| PER_CHECKLIST_ALLOCATIONS_TL | TABLE | 12 | Translation table for checklist allocation |
| PER_CHECKLIST_ALLOC_CRITERIA | TABLE | 19 | Table to store allocation criteria corresponding to a configuration used for mass assigning journeys... |
| PER_CHECKLIST_BATCH_ACTIONS | TABLE | 25 | This table stores batch actions |
| PER_CHECKLIST_BATCH_CHUNKS | TABLE | 13 | This table stores chunks of a batch action. |
| PER_CHECKLIST_BATCH_CRITERIA | TABLE | 23 | This table stores criteria of a batch action. |
| PER_CHECKLIST_CATEGORIES_B | TABLE | 19 | Table to store checklist categories. |
| PER_CHECKLIST_CATEGORIES_TL | TABLE | 15 | Translation table for PER_CHECKLIST_CATEGORIES_B |
| PER_CHECKLIST_CONTACTS | TABLE | 15 | PER_CHECKLIST_CONTACTS : This table has checklist contacts |
| PER_CHECKLIST_CONTENTS | TABLE | 13 | PER_CHECKLIST_CONTENTS : This table has checlist contents |
| PER_CHECKLIST_CONVERSATIONS | TABLE | 25 | Table to store checklist conversations. |
| PER_CHECKLIST_EXCEPTIONS | TABLE | 14 | This table records exceptions occurring at customer side |
| PER_CHECKLIST_INTEGRATIONS | TABLE | 72 | Stores the configuration details for various checklist integrations. |
| PER_CHECKLIST_PERIODS | TABLE | 15 | Table to store generated periods for allocation of checklist |
| PER_CHECKLIST_ROLE_MAPS | TABLE | 24 | Table storing role access information for a checklist template. |
| PER_CHECKLIST_SCHEDULES | TABLE | 36 | Table to store generated schedules for allocation of checklist |
| PER_CHECKLIST_SLOTS | TABLE | 11 | Table to store slots for schedules |
| PER_CHECKLIST_TASKS_B | TABLE | 92 | PER_CHECKLIST_TASKS_B : This table is base table for checklist tasks |
| PER_CHECKLIST_TASKS_TL | TABLE | 29 | PER_CHECKLIST_TASKS_TL : This is the translation table for PER_CHECKLIST_TASKS_B |
| PER_CHECKLIST_TASK_NOTIFS | TABLE | 27 | PER_CHECKLIST_TASK_NOTIFS : This table has task notifications |
| PER_CHECKLIST_USAGES | TABLE | 26 | Table to track usages of a given checklist template |
| PER_CHK_ACTION_CRITERIA | TABLE | 25 | The table records checklist events action criteria. |
| PER_CHK_ACTION_OCCURRENCES | TABLE | 21 | PER_CHK_ACTION_OCCURRENCES : Run time table to store event for allocating a checklist |
| PER_CHK_ACTION_OCC_ITEMS | TABLE | 24 | PER_CHK_ACTION_OCC_ITEMS : Run time child table fo PER_CHK_ACTION_OCCURRENCES table |
| PER_CHK_ALLOC_RESULTS | TABLE | 34 | Table to hold checklist allocation result state |
| PER_CHK_ALLOC_TASK_RESULTS | TABLE | 27 | Table to hold checklist task allocation result state |
| PER_CHK_ARCH_ALLOCATIONS | TABLE | 120 | This table records the checklists allocated to a person. These may be copied from templates in PER_C... |
| PER_CHK_ARCH_ALLOCATION_TL | TABLE | 19 | PER_CHK_ARCH_ALLOCATION_TL : This is translation table for PER_CHK_ARCH_ALLOCATIONS |
| PER_CHK_ARCH_ALLOC_CONTACTS | TABLE | 16 | PER_CHK_ARCH_ALLOC_CONTACTS : This table has contacts for allocated checklist. |
| PER_CHK_ARCH_ALLOC_CONTENTS | TABLE | 13 | PER_CHK_ARCH_ALLOC_CONTENTS : This table has contents of allocated checklist. |
| PER_CHK_ARCH_ALLOC_TASKS | TABLE | 160 | This table records the tasks within an allocated checklist to a person. These may be copied from tem... |
| PER_CHK_ARCH_ALLOC_TASKS_TL | TABLE | 26 | PER_CHK_ARCH_ALLOC_TASKS_TL : This is translation table for PER_CHK_ARCH_ALLOC_TASKS |
| PER_CHK_ARCH_ALLOC_TASK_PERF | TABLE | 19 | This table records performer details for an allocated task. |
| PER_CHK_ARCH_ALLOC_TASK_STAGES | TABLE | 20 | This table is used to store the archived rows of per_alloc_task_stages table |
| PER_CHK_ARCH_ALLOC_TSK_NTFS | TABLE | 26 | Archive table for task notifications |
| PER_CHK_CATEGORY_ROLE_MAPS | TABLE | 16 | Table storing role access information for a checklist category. |
| PER_CHK_CONFIGURATIONS | TABLE | 23 | Table to store configurations that will determine checklist behaviour. |
| PER_CHK_CONTENT_DEFNS_B | TABLE | 24 | PER_CHK_CONTENT_DEFNS_B : This is base table for checklist content definition |
| PER_CHK_CONTENT_DEFNS_TL | TABLE | 14 | PER_CHK_CONTENT_DEFNS_TL : This is a translation table for checklist content definition(s) |
| PER_CHK_CONTENT_ITEMS_B | TABLE | 14 | PER_CHK_CONTENT_ITEMS_B : This is base table for checklist content items |
| PER_CHK_CONTENT_ITEMS_TL | TABLE | 13 | PER_CHK_CONTENT_ITEMS_TL : This is translation table for PER_CHK_CONTENT_ITEMS_B |
| PER_CHK_GUIDED_RESPONSES | TABLE | 16 | Table to store guided journey responses. |
| PER_CHK_OBJECT_GROUPS | TABLE | 15 | Table to store checklist object groups. |
| PER_CHK_OBJ_GROUP_ITEMS | TABLE | 13 | Table to store checklist object group items. |
| PER_CHK_SURVEY_QSTN_SUMMARY | TABLE | 17 | Table to store survey questions summary |
| PER_CHK_SURVEY_RESPONSES | TABLE | 34 | Table to store survey journey responses |
| PER_CHK_SURVEY_RESP_SUMMARY | TABLE | 14 | Table to store survey responses summary |
| PER_CHK_TASK_COM_CONDNS_B | TABLE | 25 | Table to store completion conditions for a task |
| PER_CHK_TASK_COM_CONDNS_TL | TABLE | 11 | Translation table of PER_CHK_TASK_COM_CONDNS_B |
| PER_CHK_TASK_COM_CONDN_CRIT | TABLE | 24 | Table to store completion condition criteria for a task |
| PER_CHK_TASK_CONDITIONS | TABLE | 24 | PER_CHK_TASK_CONDITIONS: Stores condition to activate a task. |
| PER_CHK_TASK_CONDN_CRIT | TABLE | 27 | PER_CHK_TASK_CONDN_CRIT: Stores the criteria forming the condition. |
| PER_CHK_TASK_STAGES | TABLE | 13 | This table is used to store the stages of a task in task library |
| PER_CITIZENSHIPS | TABLE | 13 | This table is used to track the citizenship Information. |
| PER_CLICK_HISTORY | TABLE | 13 | This table stores the click history of a person. |
| PER_COL_AGREEMENTS_B | TABLE | 87 | This table stores Collective Agreements. Collective Agreements are agreements between workers and em... |
| PER_COL_AGREEMENTS_F | TABLE | 89 | This table stores Collective Agreements. Collective Agreements are agreements between workers and em... |
| PER_COL_AGREEMENTS_F_TL | TABLE | 13 | This table holds the translated name of Collective Agreements. |
| PER_COL_AGREEMENTS_TL | TABLE | 11 | This table holds the translated name of Collective Agreements. |
| PER_COL_AGRS_EXTRA_INFO_F | TABLE | 80 | This stores extensible data (Customer, Localization or Verticalization) for collective agreements. C... |
| PER_COMPARISON_SETS_B | TABLE | 14 | This table includes the list of data sets available for a comparison, with basic settings about who ... |
| PER_COMPARISON_SETS_TL | TABLE | 13 | This table includes the list of data sets available for a comparison with translatable information. |
| PER_CONNECTION_LINKS | TABLE | 13 | This table contains information about the person connections. |
| PER_CONTACT_EXTRA_INFO_F | TABLE | 144 | This table records the Extra Information particular to a contact relationship. |
| PER_CONTACT_RELSHIPS_F | TABLE | 159 | This table store the effective dated Person-Person relationship details for a person |
| PER_CONTRACTS_F | TABLE | 121 | This table holds general details of a contract associated to an employment agreement. This is date-t... |
| PER_COUNTRY_SECURITY_PROFILES | TABLE | 16 | Country Security Profiles Table. |
| PER_COUNTRY_SEC_PROF_COUNTRIES | TABLE | 11 | Country Security Profile Countries. |
| PER_DATA_ASGNMNTS_RULE_DTL | TABLE | 15 | This table contains the mappings of a role, data security context and data security context value. |
| PER_DATA_SEC_COMPUTE_ACL | TABLE | 10 | Temp table for compute user acl. |
| PER_DATA_SEC_PROCESS_DTLS | TABLE | 12 | per_data_sec_process_dlts to track the last successful runtime for the dataSecurity ess processes |
| PER_DELEGATED_ROLES | TABLE | 16 | Table for storing role delegation. |
| PER_DEPT_TREE_NODE | TABLE | 35 | Department Hierarchy Tree Node Table |
| PER_DEPT_TREE_NODE_CF | TABLE | 235 | This table holds the column flattened data for tree nodes of a Department tree hierarchy. |
| PER_DEPT_TREE_NODE_RF | TABLE | 28 | Department Hierarchy Tree Node RF Table. |
| PER_DIAG_BKP_ROWS | TABLE | 27 | Generic backup table for Customer Self Service Data Integrity. |
| PER_DISABILITIES_F | TABLE | 97 | Store disability information for a person. |
| PER_DOC_TYPE_SECURITY_PROFILES | TABLE | 17 | This table is contains the Document Type Security profiles created in the application. |
| PER_DOC_TYPE_SEC_PROF_DOCTYPES | TABLE | 12 | This table contains the Document Types selected in the Document Type Security Profile. |
| PER_DRIVERS_LICENSES | TABLE | 87 | This table records drivers license details of a person |
| PER_DRIVERS_LICENSE_TYPES | TABLE | 10 | This table records type information about a person's drivers licenses. |
| PER_EDIT_NAME_SETUP_B | TABLE | 20 | This table is used to hold the configuration of the fields for entering person names on the user int... |
| PER_EDIT_NAME_SETUP_TL | TABLE | 14 | This table contains translatable information about the name field's configuration. |
| PER_EMAIL_ADDRESSES | TABLE | 14 | This table stores email addresses of different types for a person. |
| PER_EMPL_CHILD_TXN_DATA | TABLE | 12 | This table stores all the child transactions data.This is not a date effective table |
| PER_EMPL_CONFIGURATIONS | TABLE | 24 | This is transcational table for storing configuration of conversion to hours based on fast formula. |
| PER_EMPL_CUSTOM_LOV_SQL | TABLE | 14 | This table stores customer sql. |
| PER_EMPL_DELETE_TXN_DATA | TABLE | 15 | This table stores data of a deleted business object. |
| PER_EMPL_OFFER_HR_TRACK | TABLE | 18 | This table stores the value of the offer assignment id along with the action's performed on this tab... |
| PER_EMPL_TRANSACTIONS | TABLE | 8 | This table stores the transaction XML CLOB data. |
| PER_ESIGN_CONFIGURATION | TABLE | 17 | This table is used for storing docusign details |
| PER_ETHNICITIES | TABLE | 13 | This table stores legislation-specific ethnicity data for a person. May be multiple rows within a Le... |
| PER_EVENTS | TABLE | 21 | Table Definition for PER_EVENTS |
| PER_EVENT_PROCESS_STAGE | TABLE | 13 | This table is used to store the event process details of Person synchronization. |
| PER_EVENT_PROCESS_STAGE_DETAIL | TABLE | 16 | This table is used to store the event process stage details during Person synchronization process. |
| PER_EXCLUSION_RULES | TABLE | 12 | PER_EXCLUSION_RULES to store Manager exclusion relates security preferences |
| PER_EXCLUSION_RULE_DTLS | TABLE | 17 | PER_EXCLUSION_RULE_DTLS to store Manager Type relates security preferences |
| PER_EXT_ACTIONS | TABLE | 23 | Captures Actions for Data Elements or Records. |
| PER_EXT_APP_IDENTIFIERS | TABLE | 16 | Stores details of the Identifiers needed to be able for Fusion HCM systems to be able to intergrate ... |
| PER_EXT_AUDIT_ACTIONS | TABLE | 12 | The table is intended for internal analysis and capture the statistics on fly based on the requireme... |
| PER_EXT_BLOCK_LINKS | TABLE | 17 | Links to capture block relationships. |
| PER_EXT_BUS_OBJECTS_B | TABLE | 17 | Extract Business Objects Base Table. |
| PER_EXT_BUS_OBJECTS_TL | TABLE | 15 | Extract Business Objects Translatable Table. |
| PER_EXT_DATA_ELEMENTS_B | TABLE | 43 | Data Elements used in extracts. |
| PER_EXT_DATA_ELEMENTS_TL | TABLE | 15 | Data Elements translatable table |
| PER_EXT_DEFINITIONS_B | TABLE | 32 | Extract Definitions base table. |
| PER_EXT_DEFINITIONS_TL | TABLE | 15 | Extract Definitions translation table. |
| PER_EXT_DEF_SAMPLES | TABLE | 19 | Extract table for Sample Definition |
| PER_EXT_DELIVERY_OPTIONS_B | TABLE | 32 | Delivery options used in Extract Definition. |
| PER_EXT_DELIVERY_OPTIONS_TL | TABLE | 15 | Delivery option translation details |
| PER_EXT_DELIVERY_OPTION_DTLS | TABLE | 16 |  |
| PER_EXT_DICT_ATTRIBUTE | TABLE | 30 | This Table will be used in Extract for Dictionary Attributes. |
| PER_EXT_DICT_DBIS | TABLE | 25 | This Table will be used in Extract for Dictionary DBI. |
| PER_EXT_DICT_OBJECT | TABLE | 33 | This Table will be used in Extract for Dictionary Objects. |
| PER_EXT_DICT_UES | TABLE | 30 | Extract Dictionary table for UEs. |
| PER_EXT_DICT_UE_BUS_OBJECTS | TABLE | 19 | Extract Dictionary table for UE Business Objects. |
| PER_EXT_FUTURE_RUN_PATTERN | TABLE | 12 | Extract Future Run Pattern table. |
| PER_EXT_LRG_OBJ_PROCESSES | TABLE | 32 | EXTRACT LARGE OBJECT PROCESSES TABLE |
| PER_EXT_PARAMETERS_B | TABLE | 30 | Parameters used in extracts definitions. |
| PER_EXT_PARAMETERS_TL | TABLE | 15 | Extract parameters translation table |
| PER_EXT_PROPERTIES | TABLE | 20 | Properties defined for an extract. |
| PER_EXT_REPLACEMENTS | TABLE | 20 | Data Element Replacement conditions and values. |
| PER_EXT_TYPES_B | TABLE | 19 | Parameters defined for an extract type. |
| PER_EXT_TYPES_TL | TABLE | 15 | Translation table for parameters of an extract type. |
| PER_EXT_TYPE_GRP_B | TABLE | 13 | Table to seed parent Extract Types to consolidate the existing Extract Types. |
| PER_EXT_TYPE_GRP_TL | TABLE | 13 | Translation table for parameters of an extract type. |
| PER_EXT_TYPE_PARAMS_B | TABLE | 21 | Parameters defined for an extract type. |
| PER_EXT_TYPE_PARAMS_TL | TABLE | 15 | Translation table for parameters of an extract type. |
| PER_EXT_UCM_PURGE_DOC | TABLE | 16 | Extract Table for capturing UCM document failed cases |
| PER_EXT_UE_DBI_MAPPING | TABLE | 23 | DBI and User Entity Mapping Table |
| PER_FLEX_MAPPING_USAGES | TABLE | 12 | This table stores the usages for each flexfield mappings. |
| PER_FLEX_SEGMENT_MAPPINGS | TABLE | 15 | This table stores mapping between source flexfields to destination flexfields. |
| PER_GENERATED_DATA_ROLES | TABLE | 18 | This table stores the information related to data roles created on a Job Role. |
| PER_GEN_DATA_ROLE_PROFILES | TABLE | 15 | This table stores the information related to assignment of Security Profiles to a Data Role. |
| PER_GEO_TREE_NODE | TABLE | 38 | Geographic Hierarchy Tree Node Table |
| PER_GEO_TREE_NODE_RF | TABLE | 28 | Geographic Hierarchy Tree Node RF Table. |
| PER_GRADES_F | TABLE | 19 | PER_GRADES_F stores the Grade definitions. Grades identify the level or rank of an employee in an or... |
| PER_GRADES_F_TL | TABLE | 13 | Contains translated attributes of PER_GRADES_F base table. |
| PER_GRADES_IN_LADDERS_F | TABLE | 14 | PER_GRADES_IN_LADDERS_F stores the Grades and the order of the grades attached to a Grade Ladder. |
| PER_GRADE_EXTRA_INFO_F | TABLE | 81 | This is an obsolete table and not in use. |
| PER_GRADE_LADDERS_F | TABLE | 43 | PER_GRADE_LADDERS_F stores the grade ladder details. A Grade Ladder is a hierarchy of Grades and is ... |
| PER_GRADE_LADDERS_F_TL | TABLE | 13 | Contains translated attributes of PER_GRADE_LADDERS_F base table. |
| PER_GRADE_LADDER_LEG_F | TABLE | 80 | This is an obsolete table and not in use. |
| PER_GRADE_LEG_F | TABLE | 80 | PER_GRADE_LEG_F stores the legislative attributes for a Grade. |
| PER_GRADE_SECURITY_PROFILES | TABLE | 14 | Grade Security Profiles Table for configuring grade related security. |
| PER_GRADE_SEC_PROFILE_GRADES | TABLE | 11 | PER_GRADE_SEC_PROFILE_GRADES table to store Grades related security preferences |
| PER_GRADE_SEC_PROF_GRD_LADDERS | TABLE | 10 | PER_GRADE_SEC_PROF_GRD_LADDERS table used to store Grade Ladder related security preferences |
| PER_GRADE_STEPS_F | TABLE | 14 | PER_GRADE_STEPS_F stores the steps within a Grade and their incremental order. |
| PER_GRADE_STEPS_F_TL | TABLE | 13 | Contains translated attributes of PER_GRADE_STEPS_F base table. |
| PER_GRADE_STEP_LEG_F | TABLE | 80 | This is an obsolete table and not in use. |
| PER_IMAGES | TABLE | 14 | This table stores images/photos for a person. |
| PER_INFO_TYPES_B | TABLE | 12 | This table stores the generic Info Types setup data. |
| PER_INFO_TYPES_TL | TABLE | 11 | This table stores the Translated Info Types setup data. |
| PER_INSTANCE_SET_MAPPINGS | TABLE | 16 | PER_INSTANCE_SET_MAPPINGS table to store mappings to FND Grants instance sets |
| PER_INTG_INBOUND_DATA | TABLE | 20 | Table to store inbound xml data received from partners and track the progress of the data in. |
| PER_INTG_INBOUND_DETAILS | TABLE | 17 | This table stores Details about the each record that was received. |
| PER_INTG_OUTBOUND_DATA | TABLE | 25 | This table is to track the Outbound data sent to Recruitment partner |
| PER_INTG_OUTBOUND_ERROR | TABLE | 15 | This table stores a row for each unsuccessful transfer of a row to the partner. |
| PER_INTG_OUTBOUND_SUCCESS | TABLE | 15 | This table stores a row for each successful transfer of a row to the partner. |
| PER_INTG_TALEO_EXPORT_M | TABLE | 110 | This table holds information about the person records that needs to be exported as part of integrati... |
| PER_INTG_USER_CAND_MAP | TABLE | 15 | Table to store notified user and candidate data and hold the mapping between the task_id and the can... |
| PER_JOBS_EIT_CATEGORY | TABLE | 7 | Jobs intermediate table storing Extensible Flexfield Category Code for each job |
| PER_JOBS_F | TABLE | 33 | PER_JOBS_F holds jobs that have been defined for an Enterprise. Jobs define the role that an employe... |
| PER_JOBS_F_TL | TABLE | 13 | Contains translated attributes of PER_JOBS_F base table. |
| PER_JOB_EVALUATIONS | TABLE | 18 | PER_JOB_EVALUATIONS holds the schemes and systems that the Enterprise uses to evaluate the jobs and ... |
| PER_JOB_EXTRA_INFO_F | TABLE | 147 | This table holds the details of extra information for a job. |
| PER_JOB_FAMILY_F | TABLE | 13 | PER_JOB_FAMILY_F holds Job Families. Job Families enable identification of related jobs that may not... |
| PER_JOB_FAMILY_F_TL | TABLE | 13 | Contains translated attributes of PER_JOB_FAMILY_F base table. |
| PER_JOB_FAMILY_SUB_FAMILIES_F | TABLE | 14 | PER_JOB_FAMILY_SUB_FAMILIES_F holds the association between Job Families and their Sub Job Families. |
| PER_JOB_LEG_F | TABLE | 80 | PER_JOB_LEG_F stores legislative attributes of jobs. |
| PER_JOB_SECURITY_PROFILES | TABLE | 15 | Job Security Profiles Main Table. |
| PER_JOB_SEC_PROFILE_JOBS | TABLE | 11 | Job Security Profile Jobs Table. |
| PER_JOB_SEC_PROF_JOB_FAMILIES | TABLE | 10 | PER_JOB_SEC_PROF_JOB_FAMILIES table to store Job Family related security preferences |
| PER_JOB_SEC_PROF_JOB_FUNCTIONS | TABLE | 10 | Job Security Profiles Job Functions. |
| PER_JOB_TEMP_USERS | TABLE | 10 | Temp table for holding users for role processing. |
| PER_KEYWORDS | TABLE | 15 | This table is used to save data collected by the keyword search crawler. |
| PER_KEYWORDS_SH | TABLE | 15 | This shadow table is used to save data collected by the keyword search crawler. |
| PER_LDAP_DATA_ASGNS | TABLE | 16 | Table for storing one record for each data access assignment to be processed |
| PER_LDAP_REQUESTS | TABLE | 21 | Table for storing one record per OIM request made by the calling system. |
| PER_LDAP_ROLES | TABLE | 20 | Table for storing one record for each Role Addition or Removal to be processed in OIM |
| PER_LDAP_ROLE_ATTR | TABLE | 10 | Table for storing extra ldap role request attributes |
| PER_LDAP_ROLE_MEMBERSHIPS | TABLE | 16 | Table for storing one record for each Role Membership to be processed in OIM when creating new users... |
| PER_LDAP_USERS | TABLE | 27 | Table for storing one record for each user to be processed in OIM when creating new users or maintai... |
| PER_LDAP_USER_ATTR | TABLE | 10 | Table for storing extra ldap user request attributes |
| PER_LDG_SECURITY_PROFILES | TABLE | 16 | Legislative Data Groups Security Profile. |
| PER_LDG_SECURITY_PROFILE_LDGS | TABLE | 11 | Legislative Data Groups Security Profile LDGs. |
| PER_LEGISLATIVE_DATA_GROUPS | TABLE | 11 | This table holds the data for all Legislative Data Groups. |
| PER_LEGISLATIVE_DATA_GROUPS_TL | TABLE | 11 | This table stores the translatable data for PER_LEGISLATIVE_DATA_GROUPS. |
| PER_LOCATIONS | TABLE | 15 | PER_LOCATIONS is the parent table.It stores generic location attributes. |
| PER_LOCATION_DETAILS_F | TABLE | 47 | PER_LOCATION_DETAILS_F stores the location details related attributes. |
| PER_LOCATION_DETAILS_F_TL | TABLE | 16 | PER_LOCATION_DETAILS_F_TL stores the translated attributes of the base table PER_LOCATION_DETAILS_F |
| PER_LOCATION_EXTRA_INFO_F | TABLE | 147 | PER_LOCATION_EXTRA_INFO_F stores the Extra Information attributes for a Location |
| PER_LOCATION_LEG_F | TABLE | 80 | PER_LOCATION_LEG_F stores the legislative attributes for a Location |
| PER_LOCATION_SECURITY_PROFILES | TABLE | 15 | Location Security Profiles Table. |
| PER_LOC_ADDRESS_USAGES_F | TABLE | 14 | PER_LOC_ADDRESS_USAGES_F stores the Address Type for an Address associated with a Location |
| PER_LOC_EIT_CATEGORY | TABLE | 8 | Table that stores the Location EIT category information. |
| PER_LOC_SEC_PROFILE_LOCATIONS | TABLE | 11 | Location Security Profile Locations. |
| PER_MANAGER_HRCHY_CF | TABLE | 54 | This table stores the column flattened manager hierarchy details. The denormalized details are deriv... |
| PER_MANAGER_HRCHY_DN | TABLE | 20 | This table stores the flattened manager hierarchy details. The denormalized details are derived from... |
| PER_MANAGER_HRCHY_DN_SPLIT | TABLE | 11 | This table is used internally to populate column flattened manager hierarchy view. This wont be expo... |
| PER_MANAGER_HRCHY_REPORTEES_DN | TABLE | 55 | This table stores the column flattened manager hierarchy details. The denormalized details are deriv... |
| PER_MASS_ACTION_HEADER | TABLE | 18 | Stores status and other general information related to a Mass Action. |
| PER_MASS_ACTION_LINES | TABLE | 275 | Stores changes done by a Mass Action. Each line corresponds to a specific set of changes done to a l... |
| PER_MASS_ERROR_LINES | TABLE | 55 | Stores error information generated during the processing of a mass action. |
| PER_MASS_LINE_FUT_UPDATES | TABLE | 22 | Stores summary of changed attribute values of different entities. |
| PER_MA_ASSIGNMENT_FLEX | TABLE | 181 | Stores assignment flex field information. This is processed by mass actions and represents data gett... |
| PER_MEDICAL_ASSESSMENTS | TABLE | 48 | This table stores the medical assessments for the person. |
| PER_NAME_STYLES_B | TABLE | 14 | This table is used to associate name style with legislation. It holds one row for the universal name... |
| PER_NAME_STYLES_TL | TABLE | 14 | This table stores the translatable description of each name style. |
| PER_NATIONAL_IDENTIFIERS | TABLE | 15 | This table records National Identifiers for the person, in different Legislation Codes, and differen... |
| PER_NUDGES | TABLE | 65 | This table records the nudges assigned to a person. |
| PER_NUDGE_ARCHIVES | TABLE | 67 | PER_NUDGE_ARCHIVES : this table records the nudges assigned to a person. |
| PER_NUDGE_CHANNEL_DETAILS | TABLE | 24 | This table records the channel details of the assigned nudges. |
| PER_NUDGE_CHNL_DTL_ARCHIVES | TABLE | 23 | PER_NUDGE_CHNL_DTL_ARCHIVES : this table records the channel details of the assigned nudges. |
| PER_NUDGE_EVENT_OCCURRENCES | TABLE | 12 | This table records the nudge event occurrences. |
| PER_NUDGE_PLANS_B | TABLE | 24 | This table records the nudge plans. |
| PER_NUDGE_PLANS_TL | TABLE | 12 | PER_NUDGE_PLANS_TL : This is translation table for PER_NUDGE_PLANS_B. |
| PER_NUDGE_PLAN_CRITERIA | TABLE | 22 | This table stores the information of the criteria for a nudge. |
| PER_NUDGE_PLAN_EXECUTIONS | TABLE | 19 | This table records the information of nudge plan executions. |
| PER_NUDGE_PLAN_EXEC_STATS | TABLE | 14 | This table records the nudges execution status information. |
| PER_NUDGE_PLAN_NDG_CHNLS_B | TABLE | 41 | This table records the nudge channel details for a nudge plan. |
| PER_NUDGE_PLAN_NDG_CHNLS_TL | TABLE | 13 | PER_NUDGE_PLAN_NDG_CHNLS_TL : This is the translation table to store the information of nudge channe... |
| PER_NUDGE_PLAN_NUDGES_B | TABLE | 37 | This table stores the nudge plan details. |
| PER_NUDGE_PLAN_NUDGES_TL | TABLE | 12 | PER_NUDGE_PLAN_NUDGES_TL : This is the translation table to store the information of nudge plans. |
| PER_NUDGE_PLAN_OBJECTS | TABLE | 15 | This table records the nudge plan objects. |
| PER_NUDGE_PLAN_POPULATION | TABLE | 13 | This table records the nudge plan population. |
| PER_OBJECT_NUDGES | TABLE | 65 | This table records the nudges assigned to an object. |
| PER_OBJ_NUDGE_ARCHIVES | TABLE | 67 | PER_OBJ_NUDGE_ARCHIVES : this table records the nudges assigned to an object. |
| PER_ORG_SECURITY_PROFILES | TABLE | 27 | Organization Security Profiles. |
| PER_ORG_SEC_PROFILE_CLASSES | TABLE | 11 | Organization Security Profile Organization Classifications. |
| PER_ORG_SEC_PROFILE_ORGS | TABLE | 12 | Organization Security Profile Organizations. |
| PER_ORG_TREE_NODE | TABLE | 35 | Organization Hierarchy Tree Node Table |
| PER_ORG_TREE_NODE_CF | TABLE | 235 | This table holds the column flattened data for tree nodes of a Organization tree hierarchy. |
| PER_ORG_TREE_NODE_RF | TABLE | 28 | Organization Hierarchy Tree Node RF Table. |
| PER_PASSPORTS | TABLE | 84 | This table stores images/photos for a person. |
| PER_PAY_SCALES | TABLE | 9 | PER_PAY_SCALES stores the Pay Scale details. A Pay Scale is a sequence of Points that determine the ... |
| PER_PAY_SCALES_TL | TABLE | 10 | Contains translated attributes of PER_PAY_SCALES base table. |
| PER_PAY_SCALE_LEG | TABLE | 41 | PER_PAY_SCALE_LEG stores the legislative attributes for a Pay Scale. |
| PER_PAY_SCALE_POINTS | TABLE | 9 | PER_PAY_SCALE_POINTS stores the list of Pay Scale Points of a Pay Scale and their incremental order.... |
| PER_PAY_SCALE_POINTS_TL | TABLE | 10 | Contains translated attributes of PER_PAY_SCALE_POINTS base table. |
| PER_PAY_SCALE_POINT_LEG | TABLE | 41 | PER_PAY_SCALE_POINT_LEG stores the legislative attributes for a Pay Scale Point. |
| PER_PEOPLE_EXTRA_INFO_F | TABLE | 145 | This table stores effective-dated Extra Information Type data, which consist mainly of legislative p... |
| PER_PEOPLE_GROUPS | TABLE | 44 | This table contains the people group flexfield segment values for individual employee assignments. |
| PER_PEOPLE_LEGISLATIVE_F | TABLE | 82 | This table stores legislative-specific Core person data, including that which is currently defined i... |
| PER_PERIODS_OF_SERVICE | TABLE | 101 | This table stores all information related to the person?s Work Relationships. An Work Relationship d... |
| PER_PERSONS | TABLE | 19 | This table is new for Fusion, and is created to assist BC4J architecture by providing a non-date tra... |
| PER_PERSON_ADDR_USAGES_F | TABLE | 13 | This table is used to store the person address usages records. |
| PER_PERSON_DLVRY_METHODS | TABLE | 15 | Communication delivery methods for the person, also storing preferred communication language |
| PER_PERSON_LOC_FLOW_CONFIG | TABLE | 19 | This table stores person sensitive information localization seed data. Localizations can use the see... |
| PER_PERSON_NAMES_F | TABLE | 94 | This table is to hold core (common) and legislative-specific name components for a person, and names... |
| PER_PERSON_RELATIONSHIPS | TABLE | 12 | This table is used to store the relationship details of a person with respect to another person in t... |
| PER_PERSON_SECURITY_PROFILES | TABLE | 57 | Person Security Profile Table-Each Record stores conditions used to generate instance set based on p... |
| PER_PERSON_SEC_PROF_MGR_TYPES | TABLE | 11 | PER_PERSON_SEC_PROF_MGR_TYPES to store Manager Type relates security preferences |
| PER_PERSON_SEC_PROF_PER_TYPES | TABLE | 17 | Person Security Profile Person Types |
| PER_PERSON_TYPES | TABLE | 17 | Setup table defining the relationship between system person types and user variations of those. |
| PER_PERSON_TYPES_TL | TABLE | 14 | This table stores translated attributes related to PER_PERSON_TYPES |
| PER_PERSON_TYPE_USAGES_M | TABLE | 16 | This table is used to store the person type information for a person's relationship to the business ... |
| PER_PHONES | TABLE | 20 | This table stores phone numbers of different types for a person. |
| PER_PORTRAIT_CARD_CONFIG | TABLE | 11 | This table is new for Fusion, and has been created to handle user card order in portrait. |
| PER_PORTRAIT_CONTENT_B | TABLE | 24 | This table is new for Fusion,And has been created to handle user preferences to choose whether to sh... |
| PER_PORTRAIT_CONTENT_TL | TABLE | 15 | This table stores the Translated Portrait Content data. |
| PER_PORTRAIT_MESSAGES_B | TABLE | 18 | This table stores administrator messages that should appear on the Portrait Pages. |
| PER_PORTRAIT_MESSAGES_TL | TABLE | 11 | This is the translatable table for Portrait messages. |
| PER_PORTRAIT_PREFERENCES | TABLE | 13 | This table sores the Portrait Content preferences for person. |
| PER_POSITION_BUDGETS | TABLE | 16 | Position Budgets table that stores allocated values for headcount, FTE & amount. |
| PER_POSITION_BUDGETS_TL | TABLE | 10 | Position Budgets table that stores the translatable position budget attributes. |
| PER_POSITION_EXTRA_INFO_F | TABLE | 147 | Position Extra Information table |
| PER_POSITION_HIERARCHY_F | TABLE | 13 | This table will be used to store position hierarchy information. |
| PER_POSITION_HRCHY_RF | TABLE | 11 | This table stores Position Hierarchy Row Flattened Data |
| PER_POSITION_HRCHY_RF_SH | TABLE | 11 | This table stores Position Hierarchy Row Flattened Data |
| PER_POSITION_LEG_F | TABLE | 80 | Table storing Position legislative data |
| PER_POSITION_PENDING_TXNS | TABLE | 12 | The table will store the data about status of changes done on different positions from Graphical Pos... |
| PER_POSITION_SECURITY_PROFILES | TABLE | 35 | Position Security Profiles Table. |
| PER_POS_EIT_CATEGORY | TABLE | 7 | Table to hold category information for Position EIT EFF. |
| PER_POS_FUNDING_POSITIONS_F | TABLE | 13 | This table stores relationships between positions and their funding positions |
| PER_POS_SECPRF_AORSCOPE | TABLE | 11 | Position Security Profile AOR Scopes Table: This table will hold scope of areas of responsibility pr... |
| PER_POS_SEC_PROFILE_POSITIONS | TABLE | 13 | Position Security Profile Positions |
| PER_POS_TREE_NODE | TABLE | 35 | Position Hierarchy Tree Node Table |
| PER_POS_TREE_NODE_CF | TABLE | 235 | This table holds the column flattened data for tree nodes of a Position tree hierarchy. |
| PER_POS_TREE_NODE_RF | TABLE | 28 | Position Hierarchy Tree Node RF Table. |
| PER_PREVIOUS_EMPLOYERS | TABLE | 83 |  |
| PER_PREVIOUS_JOBS | TABLE | 79 |  |
| PER_PREVIOUS_JOB_USAGES | TABLE | 78 | This table holds information about which previous jobs are relevant to a particular employee assignm... |
| PER_PREV_JOB_EXTRA_INFO | TABLE | 71 | Extra information for Jobs held with previous employers |
| PER_PRSN_SEC_MATRLZED_CACHE | TABLE | 4 | This table will hold materialized cache data for list of persons a user has access to. |
| PER_PRSN_SEC_PROF_AOR_SCOPES | TABLE | 17 | Person Security Profile AOR Scopes Table: This table will hold scope of areas of responsibility pref... |
| PER_PRSN_SEC_PROF_EXCLUSIONS | TABLE | 10 | PER_PERSON_SEC_PROF_EXCLUSIONS to store exclusion relates security preferences |
| PER_PUBLIC_PRSN_SEC_PROFILES | TABLE | 33 | Public Person Security Profile Table-Each Record stores conditions used to generate security conditi... |
| PER_PUBLIC_PRSN_SEC_PROF_ASGS | TABLE | 10 | Public Person Security Profile assignment Table. Each Record stores role assigned. |
| PER_PUBLIC_PRSN_SEC_PROF_DTLS | TABLE | 16 | Public Person Security Profile Detail Table-Each Record stores conditions used to generate security ... |
| PER_RATES_F | TABLE | 23 | PER_RATES_F stores the Rate definitions for Grade, Scale or Step Rates where the type of rate is det... |
| PER_RATES_F_TL | TABLE | 13 | Contains translated attributes of PER_RATES_F base table. |
| PER_RATE_VALUES_F | TABLE | 86 | PER_RATE_VALUES_F stores the Grade, Scale or Step Rate values for a specific Grade, Pay Scale Point ... |
| PER_RELIGIONS | TABLE | 12 | This table stores legislation-specific religion data for a person. May be multiple rows within a Leg... |
| PER_REP_DOCUMENTS_B | TABLE | 12 | HCM Reporting documents for Delivery Options. |
| PER_REP_DOCUMENTS_TL | TABLE | 12 | HCM Reporting documents translation table |
| PER_REP_LEVEL_HIERARCHY | TABLE | 11 | HCM Reporting document preference level hierarchy |
| PER_REP_PREFERENCES | TABLE | 16 | HCM Reporting document delivery preferences |
| PER_RESOURCE_EXCEPTIONS | TABLE | 12 | This tables holds the resource exception data used during schedule assignment to resources |
| PER_ROLES_DN | TABLE | 20 | Stores the roles that are used in the system. Data normally denormalized from LDAP via the Identity ... |
| PER_ROLES_DN_TL | TABLE | 12 | Translated role names for roles used in the system |
| PER_ROLE_MAPPINGS | TABLE | 48 | Stores the mappings of the different roles. |
| PER_ROLE_MAPPING_ROLES | TABLE | 13 | Stores the reference between Roles and Role Mappings |
| PER_SCHEDULE_ASSIGNMENTS | TABLE | 15 | This table holds Schedule assignment data for each resource |
| PER_SCHEDULE_ELIGIBILITY | TABLE | 10 | This Table stores the eligibility profiles associated to schedules |
| PER_SCHEDULE_EXCEPTIONS | TABLE | 14 | This table holds the exception details for every schedule and schedule assignment. The exception can... |
| PER_SCH_INHERIT_HIER | TABLE | 14 | THis table hols the hierarchy order and sequence of levels based on which Schedule has to be retriev... |
| PER_SEARCH_FILTERS | TABLE | 12 | Table to store public person security profile search filter. |
| PER_SEARCH_FILTER_MAPPINGS | TABLE | 12 | Table to store public person security profile search filter mapping. |
| PER_SEARCH_FILTER_QUERY_MAP | TABLE | 13 | Table to store query maps for references used in generated search filter. |
| PER_SEARCH_OBJECTS | TABLE | 18 | This table holds named query statements used to populate the table PER_KEYWORDS. The statements are ... |
| PER_SECURING_OBJECTS | TABLE | 18 | This table stores the mapping between Fnd Objects and Hr Securing Objects. This information will be ... |
| PER_SEC_PROF_PRED_TEMPLATES | TABLE | 17 | Person Security Profiles Predicate Templates: This table will hold predicate templates for different... |
| PER_SENIORITY_DATES | TABLE | 66 | This is transactional table for storing seniority dates. |
| PER_SENIORITY_DATES_F | TABLE | 52 | This is transactional table for storing seniority dates. |
| PER_SENIORITY_DATES_SETUP | TABLE | 42 | This table stores the configuration for the Seniority Items. Whenever the user creates the new Senio... |
| PER_SENIORITY_HOURS | TABLE | 16 | This is transactional table for storing seniority hours from Payroll or OTL. |
| PER_SENSITIVE_DATA_AUDIT | TABLE | 20 | This table is new for Fusion, and has been created to store the sensitive data audit. |
| PER_SHARE_INFORMATION | TABLE | 22 | This table records the items of personal, employment etc., information are to be shared for a given ... |
| PER_SHARE_INFO_COMPONENTS | TABLE | 12 | This table records the items of personal, employment etc., information that is shared for a given in... |
| PER_SRM_HISTORY | TABLE | 13 | The table stores the role hierarchy changes processed by Generate Role Hierarchy process in policy s... |
| PER_SRM_ROLE_MEMBERSHIPS | TABLE | 17 | The table stores the role membership mappings to product offerings, options and features that are pr... |
| PER_SRM_RUNS | TABLE | 10 | The table stores the information of each run of Generate Role Hierarchy process. |
| PER_TALEO_IMPORT_RESULTS | TABLE | 34 | This table stores information about successful candidates imported from Taleo to Fusion |
| PER_TASKS_IN_CHECKLIST_B | TABLE | 131 | This table records the tasks within the checklist templates. |
| PER_TASKS_IN_CHECKLIST_TL | TABLE | 29 | PER_TASKS_IN_CHECKLIST_TL holds translated information for Checklist Templates. |
| PER_TASK_ACTIONS_B | TABLE | 18 | PER_TASK_ACTIONS_B: Actions related to a particular task. |
| PER_TASK_ACTIONS_TL | TABLE | 15 | PER_TASK_ACTIONS_TL : Translation table of PER_TASK_ACTIONS_B |
| PER_TASK_DEPENDENCIES | TABLE | 19 | PER_TASK_DEPENDENCIES : This table holds dependent task details |
| PER_TASK_LIB_COM_CONDNS_B | TABLE | 25 | Table to store completion conditions for a task library task |
| PER_TASK_LIB_COM_CONDNS_TL | TABLE | 11 | Translation table of PER_TASK_LIB_COM_CONDNS_B |
| PER_TASK_LIB_COM_CONDN_CRIT | TABLE | 23 | Table to store completion condition criteria for a task library task |
| PER_TASK_NOTIFICATIONS | TABLE | 30 | PER_TASK_NOTIFICATIONS : This table has task notifications |
| PER_TASK_STAGES | TABLE | 13 | This table is used to store the stages of a task in checklist |
| PER_USERS | TABLE | 22 | Table for storing one record per fusion system user. Maps to a single LDAP user unless the user is d... |
| PER_USER_HISTORY | TABLE | 16 | Table for storing the history of a user record (changes to username and GUID over time) |
| PER_USER_ROLES | TABLE | 16 | Table for storing one record for each Role Membership that the user has been provisioned in LDAP. |
| PER_VALID_GRADES_F | TABLE | 14 | Date Effective Valid Grades table |
| PER_VISAS_PERMITS_F | TABLE | 91 | This table supports storage of visa, work permit and residency data |
| PER_WORKING_HOUR_PATTERNS_F | TABLE | 85 | This table contains Work Hour Patterns data. |
| PER_WORK_INCIDENTS | TABLE | 94 | This table stores details of incidents at work, dates, place, types |
| RA_ACCOUNT_DEFAULTS_ALL | TABLE | 9 | The RA_ACCOUNT_DEFAULTS_ALL table stores AutoAccounting setup information. Each row represents an ac... |
| RA_ACCOUNT_DEFAULT_SEGMENTS | TABLE | 12 | The RA_ACCOUNT_DEFAULT_SEGMENTS table stores AutoAccounting setup information. Each row in this tabl... |
| RA_BATCHES_ALL | TABLE | 33 | The RA_BATCHES_ALL table stores information about each invoice or bills receivable batch that you en... |
| RA_BILL_PLANS_ALL | TABLE | 47 | RA_BILL_PLANS_ALL contains information about recurring bill plans, including billing frequency, cont... |
| RA_BILL_PLAN_HISTORY | TABLE | 16 | RA_BILL_PLAN_HISTORY contains the historical record of changes to the attributes of a recurring bill... |
| RA_BILL_PLAN_LINES_ALL | TABLE | 39 | RA_BILL_PLAN_LINES_ALL contains the changes to a recurring bill plan, including amount to credit, qu... |
| RA_CM_REQUESTS_ALL | TABLE | 47 | The RA_CM_REQUESTS_ALL table contains information for credit memo requests during the invoice disput... |
| RA_CM_REQUEST_LINES_ALL | TABLE | 28 | The RA_CM_REQUEST_LINES_ALL table contains information about specific invoice lines that a customer ... |
| RA_CUST_RECEIPT_METHODS | TABLE | 17 | The RA_CUST_RECEIPT_METHODS table contains a row for each receipt method assigned to a customer or c... |
| RA_GROUPING_RULES | TABLE | 16 | The RA_GROUPING_RULES table stores grouping rules used by AutoInvoice. Grouping rules determine how ... |
| RA_GROUPING_TRX_TYPES | TABLE | 12 | The RA_GROUPING_TRX_TYPES table is an intersection of grouping rules, as defined in the RA_GROUPING_... |
| RA_GROUP_BYS | TABLE | 11 | The RA_GROUP_BYS table holds a row for every column that each grouping rule uses to group invoice li... |
| RA_GROUP_BY_COLUMNS | TABLE | 15 | The RA_GROUP_BY_COLUMNS table stores the list of columns that AutoInvoice can use to group interface... |
| RA_LINE_ORDERING_RULES | TABLE | 14 | The RA_LINE_ORDERING_RULES table represents a line ordering rule in each row. A line ordering rule i... |
| RA_LINE_ORDER_BYS | TABLE | 13 | The RA_LINE_ORDER_BYS table contains a row for each column that you define to be part of an AutoInvo... |
| RA_LINE_ORDER_BY_COLUMNS | TABLE | 12 | The RA_LINE_ORDER_BY_COLUMNS table stores the columns that can be used to define AutoInvoice line or... |
| RA_RECURRING_BILL_PLANS | TABLE | 33 | Recurring Bill Plan stores the information about recurring bills such as amount per bill, number of ... |
| RA_RECURRING_BILL_PLAN_LINES | TABLE | 30 | This table contains the changes to a recurring bill plan, such as the amount to credit, quantity to ... |
| RA_RECUR_INTERIM | TABLE | 15 | The RA_RECUR_INTERIM table temporarily holds invoices that Oracle Receivables will copy in the futur... |
| RA_REMIT_TOS_ALL | TABLE | 16 | The RA_REMIT_TOS_ALL table stores information to link a remit-to address with a state and country. O... |
| RA_RULES | TABLE | 20 | The RA_RULES table stores invoicing and accounting rules. Receivables creates one row in this table ... |
| RA_RULE_SCHEDULES | TABLE | 14 | The RA_RULE_SCHEDULES table stores revenue recognition schedules for invoices with accounting rules.... |
| RA_TERMS_LINES_DISCOUNTS | TABLE | 16 | The RA_TERMS_LINES_DISCOUNTS table stores discount information for each row in the RA_TERMS_LINES ta... |
| RA_TERMS_TL | TABLE | 15 | The RA_TERMS_TL table provides multilingual support for each payment term you define in Oracle Recei... |
| RG_TABLE_SIZES | TABLE | 8 | Sizes of selected Oracle Fusion General Ledger tables. |
| VRM_ACCOUNTING_EVENTS | TABLE | 32 | This table contains the accounting events of customer contract. |
| VRM_APP_SOURCES | TABLE | 12 | This table contains the application sources and their start dates for integration with Oracle Fusion... |
| VRM_AR_BATCH_SOURCES | TABLE | 12 | This table contains the transaction sources and their start dates for integration with Oracle Fusion... |
| VRM_BILLING_LINE_APPLICATIONS | TABLE | 15 | This table contains the billing application details to source document lines. |
| VRM_BILLING_LINE_DETAILS | TABLE | 47 | This table contains the billing information for performance obligation lines. |
| VRM_BILL_REV_RECON_HISTORY | TABLE | 44 | VRM_BILL_REV_RECON_HISTORY contains the history of the Billing and Revenue information for all the s... |
| VRM_CARVEOUT_ADJ_INTERIM | TABLE | 73 | The VRM_CARVEOUT_ADJ_INTERIM table contains information about revenue adjustments created as a resul... |
| VRM_CARVEOUT_THRESHOLD_AMTS_F | TABLE | 11 | VRM_CARVEOUT_THRESHOLD_AMTS_F contains the MEA adjustment threshold level determines which MEA adjus... |
| VRM_CONTRACT_ACTIVITIES | TABLE | 15 | This table contains the revenue related activities happenned of customer contract. |
| VRM_CONTRACT_ALLOC_INTERIM | TABLE | 47 | This table contains contract allocation processing-related information. |
| VRM_CONTRACT_RULES_B | TABLE | 16 | This table contains the rules for identification of customer contract. |
| VRM_CONTRACT_RULES_TL | TABLE | 14 | This table contains information about translated customer contract identification rules. |
| VRM_CONTRACT_RULE_DETAILS | TABLE | 19 | This table contains customer contract identification rule details. |
| VRM_CONTRACT_UPDATE_TPLT_B | TABLE | 13 | This table contains the templates used in revenue contract modification. |
| VRM_CONTRACT_UPDATE_TPLT_TL | TABLE | 11 | This table contains information about translated revenue contract modification templates. |
| VRM_CONTR_CARVEOUT_HDRS | TABLE | 24 | This table contains the discount header information for performance obligation. |
| VRM_CONTR_CARVEOUT_LINES | TABLE | 43 | This table contains the discount line information for performance obligation line. |
| VRM_CONTR_UPD_TPLT_RULES_B | TABLE | 12 | This table contains the updated template rules used in revenue contract modification. |
| VRM_CONTR_UPD_TPLT_RULES_TL | TABLE | 11 | This table contains information about translated revenue contract modification template rules. |
| VRM_CREATE_EVENT_DISTS_INTERIM | TABLE | 80 | This is a temporary table which is used internally by Oracle. |
| VRM_CREATE_SATIS_EVENT_INTERIM | TABLE | 52 | This table contains create satisfaction event processing-related information. |
| VRM_CREDIT_DOC_AMOUNTS | TABLE | 10 | VRM_CREDIT_DOC_AMOUNTS contains information about credit amount of a revenue document. |
| VRM_CUSTOMER_CONTRACT_AUDIT | TABLE | 33 | This table contains audit information for customer contract. |
| VRM_CUSTOMER_CONTRACT_HEADERS | TABLE | 61 | This table contains the header attributes of the customer contract. |
| VRM_DEFERRED_REV_LINES_ALL | TABLE | 20 | The VRM_DEFERRED_REV_LINES_ALL contains invoice status changes, as invoices move through the revenue... |
| VRM_DEVOLVED_PERF_OBLIG_DTLS | TABLE | 23 | This table contains summary information about promised detail lines for devolved performance obligat... |
| VRM_DOCUMENT_DATA_OBJECTS | TABLE | 18 | VRM_DOCUMENT_DATA_OBJECTS contains the database views for extracting data from the source applicatio... |
| VRM_DOC_ATTRIBUTES_B_F | TABLE | 25 | VRM_DOC_ATTRIBUTES_B_F contains the list of source document and its line attributes and their mappin... |
| VRM_DOC_ATTRIBUTES_TL | TABLE | 10 | VRM_DOC_ATTRIBUTES_TL contains translated information for VRM_DOC_ATTRIBUTES_B_F. |
| VRM_EBIZ_GL_BALANCES | TABLE | 52 | This table contains period balances information for VRM Oracle EBS GL integration. |
| VRM_EBIZ_GL_IMPORT_REFERENCES | TABLE | 12 | This table contains subledger link information for VRM Oracle EBS GL integration. |
| VRM_EBIZ_GL_JE_HDR_LINES | TABLE | 64 | This table contains journal header, line and journal batch information for VRM Oracle EBS GL integra... |
| VRM_EXTRACTION_PERIODS | TABLE | 11 | VRM_EXTRACTION_PERIODS contains the definition of extraction periods. |
| VRM_EXTRACT_LINES | TABLE | 55 | VRM_EXTRACT_LINES contains source document lines that have been extracted into the VRM application. |
| VRM_EXTRACT_RUN_DATES | TABLE | 15 | VRM_EXTRACT_RUN_DATES contains VSOE price basis data set extraction run details. |
| VRM_FAIR_PRICE_INTERIM | TABLE | 31 | VRM_FAIR_PRICE_INTERIM contains information about fair market value calculation process. |
| VRM_FMV_DATA_SET_USAGES | TABLE | 30 | VRM_FMV_DATA_SET_USAGES contains price basis data sets used for fair market value calculation proces... |
| VRM_FMV_LINES | TABLE | 65 | This object stores the fair market values (FMV). |
| VRM_FMV_LINE_SETS | TABLE | 43 | VRM_FMV_LINE_SETS contains fair market value (FMV) line sets. FMV lines are grouped into a set using... |
| VRM_FMV_SET_USAGE_REF_LINES | TABLE | 9 | The VRM_FMV_SET_USAGE_REF_LINES table contains information about reference lines adjusted for the st... |
| VRM_FMV_TEMPLATES_B | TABLE | 25 | This object stores the processing options for VSOE fair value calculation. The VSOE template is then... |
| VRM_FMV_TEMPLATES_TL | TABLE | 11 | VRM_FMV_TEMPLATES_TL contains information about translated fair market value templates. |
| VRM_FMV_TEMPL_ASSIGNMENTS | TABLE | 25 | VRM_FMV_TEMPL_ASSIGNMENTS contains assignments of VSOE templates to items. |
| VRM_FMV_TEMPL_PRC_ASSIGNMENTS | TABLE | 14 | VRM_FMV_TEMPL_PRC_ASSIGNMENTS contains pricing bands assigned to a FMV profile or item type. Each ro... |
| VRM_FP_DATA_SETS_INTERIM | TABLE | 11 | VRM_FP_DATA_SETS_INTERIM contains price basis data sets, which are in the process of FMV calculation... |
| VRM_FP_TEMPLATES_INTERIM | TABLE | 18 | VRM_FP_TEMPLATES_INTERIM contains the templates which are in the process of FMV calculation. |
| VRM_IDENTIFY_CONTRACT_INTERIM | TABLE | 271 | This is a temporary table which is used internally by Oracle. |
| VRM_IDENTIFY_MEA_INTERIM | TABLE | 127 | This object stores the header attributes of the multiple element arrangements. |
| VRM_IMPL_PERF_OBLIG_TLINES | TABLE | 23 | This table contains implied performance obligation line details. |
| VRM_IMPL_PERF_OBLIG_TPLT_B | TABLE | 17 | This table contains the implied performance obligation templates. |
| VRM_IMPL_PERF_OBLIG_TPLT_TL | TABLE | 11 | This table contains information about translated implied performance obligation templates. |
| VRM_ITEM_BUNDLES_B | TABLE | 8 | VRM_ITEM_BUNDLES_B contains the item bundle identifier and its status. |
| VRM_ITEM_BUNDLES_TL | TABLE | 11 | VRM_ITEM_BUNDLES_TL contains translated information for VRM_ITEM_BUNDLES_B. |
| VRM_ITEM_BUNDLE_ASSIGMENTS | TABLE | 10 | VRM_ITEM_BUNDLE_ASSIGMENTS contains information on item assignment to a bundle. |
| VRM_ITEM_GROUPS_B | TABLE | 8 | VRM_ITEM_GROUPS_B contains item group definition. Users can group a set of similar items into an ite... |
| VRM_ITEM_GROUPS_TL | TABLE | 11 | VRM_ITEM_GROUPS_TL contains information about translated item groups. |
| VRM_ITEM_GRP_ASSIGNMENTS | TABLE | 14 | This object stores assignment of items to item groups |
| VRM_LEDGER_OPTIONS | TABLE | 22 | This table contains ledger options information. |
| VRM_LINE_GROUPS | TABLE | 23 | New entity for storing of line groups along with aggregate columns. |
| VRM_MEA_DOC_ACTION_HISTORY | TABLE | 18 | VRM_MEA_DOC_ACTION_HISTORY contains action history of multiple element arrangements at both header a... |
| VRM_MEA_DOC_CARVEOUT_HDRS | TABLE | 23 | VRM_MEA_DOC_CARVEOUT_HDRS contains carve out adjustment details of multiple element arrangements. |
| VRM_MEA_DOC_CARVEOUT_LINES | TABLE | 45 | This object stores the compliance carveouts for Multiple Element Arrangements. |
| VRM_MEA_DOC_HEADERS | TABLE | 39 | This object stores the header attributes of the multiple element arrangements. |
| VRM_MEA_DOC_LINES | TABLE | 35 | This is an extension object to document lines that store processing results of all the processes ope... |
| VRM_MEA_RULES_B | TABLE | 14 | VRM_MEA_RULES_B contains the rules for identification of multiple element arrangements. |
| VRM_MEA_RULES_TL | TABLE | 11 | VRM_MEA_RULES_TL contains information about translated MEA rules. |
| VRM_MEA_RULE_DETAILS | TABLE | 16 | VRM_MEA_RULE_DETAILS contains MEA identification rule details. |
| VRM_MEA_THRESHOLD_AMTS_F | TABLE | 11 | VRM_MEA_THRESHOLD_AMTS_F contains the MEA compliance threshold level to determine which MEA complian... |
| VRM_NEW_APP_SOURCES | TABLE | 15 | This table contains application sources information. |
| VRM_NEW_AR_SOURCES | TABLE | 14 | This table contains Oracle Fusion Receivables sources information. |
| VRM_NEW_SYSTEM_OPTIONS | TABLE | 20 | This table contains system options information for Oracle Fusion Revenue Management. |
| VRM_PERF_OBLIGATIONS | TABLE | 90 | This table contains the performance obligations of customer contract. |
| VRM_PERF_OBLIGATION_LINES | TABLE | 107 | This table contains the performance obligation lines of customer contract. |
| VRM_PERF_OBLIGATION_LIN_DISTS | TABLE | 36 | This table contains the performance obligation line distribution information. |
| VRM_PERF_OBLIGATION_LIN_SPLITS | TABLE | 22 | This table contains the performance obligation line split information. |
| VRM_PERF_OBLIG_GRP_RULES_B | TABLE | 19 | This table contains the rules for identification of performance obligations. |
| VRM_PERF_OBLIG_GRP_RULES_TL | TABLE | 14 | This table contains information about translated performance obligation identification rules. |
| VRM_PERF_OBLIG_GRP_RULE_DTLS | TABLE | 16 | This table contains performance obligation identification rule details. |
| VRM_PERF_OBLIG_TEMPLATES_B | TABLE | 19 | This table contains information about the performance obligation templates. |
| VRM_PERF_OBLIG_TEMPLATES_TL | TABLE | 11 | This table contains information about translated performance obligation templates. |
| VRM_PERF_OBLIG_TEMPL_ASSIGNS | TABLE | 12 | This table contains information about performance obligation template assignment details. |
| VRM_PERIODS | TABLE | 12 | The VRM_PERIODS table contains information about accounting periods. |
| VRM_PERIOD_TYPES | TABLE | 8 | The VRM_PERIOD_TYPES table contains information about accounting period types. |
| VRM_POL_BILLING_EVENTS | TABLE | 20 | This table contains performance obligation line billing events information for customer contract. |
| VRM_POL_IMMATERIAL_DETAILS | TABLE | 40 | This table contains the actions performed on the promised detail lines of customer contract because ... |
| VRM_POL_SATISFACTION_EVENTS | TABLE | 34 | This table contains performance obligation line satisfaction events information for customer contrac... |
| VRM_PO_ASSET_LIAB_NETTING | TABLE | 41 | This table contains the netting details of the Contract Asset and Contract Liability accounts for pe... |
| VRM_PO_IMMATERIAL_DETAILS | TABLE | 25 | This table contains the actions performed on the performance obligations of customer contract becaus... |
| VRM_PO_NETTING_RUN_HISTORY | TABLE | 12 | This table contains the history of when the Contract Asset and Liability Netting for Revenue Contrac... |
| VRM_PO_REASSIGNMENT_DETAILS | TABLE | 24 | This table contains the details of performance obligations that are reassigned from source revenue c... |
| VRM_PRICE_BASIS_DATA_SETS | TABLE | 30 | VRM_PRICE_BASIS_DATA_SETS contains VSOE price basis data sets. The source documents are grouped into... |
| VRM_PRICE_EFF_PERIODS_B | TABLE | 13 | VRM_PRICE_EFF_PERIODS_B contains price effectivity periods for fair market values. |
| VRM_PRICE_EFF_PERIODS_TL | TABLE | 13 | VRM_PRICE_EFF_PERIODS_TL contains translated information for VRM_PRICE_EFF_PERIODS_B. |
| VRM_PRICE_LINE_EXCEPTIONS | TABLE | 14 | VRM_PRICE_LINE_EXCEPTIONS contains error details of VSOE price basis lines. |
| VRM_PRICE_SEGMENT_ASSIGNS | TABLE | 42 | VRM_PRICE_SEG_ASSIGNS contains assignment of source document attribute to the pricing dimension segm... |
| VRM_PRICE_SEG_ASSIGNMENTS | TABLE | 13 | VRM_PRICE_SEG_ASSIGNMENTS contains assignment of source document attributes to the pricing dimension... |
| VRM_PRICE_SEG_ASSIGN_HDRS_B | TABLE | 10 | VRM_PRICE_SEG_ASSIGN_HDRS_B contains dimension assignment created for a pricing dimension structure.... |
| VRM_PRICE_SEG_ASSIGN_HDRS_TL | TABLE | 11 | VRM_PRICE_SEG_ASSIGN_HDRS_TL provides multilingual support (MLS) for each dimension assignment. MLS ... |
| VRM_PRICING_BANDS | TABLE | 22 | VRM_PRICING_BANDS contains the pricing dimension bands. |
| VRM_PRICING_BANDS_HDRS_B | TABLE | 15 | VRM_PRICING_BANDS_HDRS_B contains pricing band created for a qualifier. A qualifier can have multipl... |
| VRM_PRICING_BANDS_HDRS_TL | TABLE | 14 | VRM_PRICING_BANDS_HDRS_TL provides multilingual support (MLS) for each pricing band. MLS enables you... |
| VRM_PRICING_COMBINATIONS | TABLE | 48 | VRM_PRICING_COMBINATIONS contains pricing dimension combinations. |
| VRM_PRICING_LINES | TABLE | 94 | This is an extension object to document lines that store the processing results of Dimension Value A... |
| VRM_PRICING_LINES_INTERIM | TABLE | 43 | VRM_PRICING_LINES_INTERIM contains source document lines, which are included in the current pricing ... |
| VRM_RECON_SUMMARY_CCID | TABLE | 13 | VRM_RECON_SUMMARY_CCID stores the Revenue Management(VRM) General Ledger account code combination fo... |
| VRM_REFERENCE_CURRENCY_DETAILS | TABLE | 61 | This table contains the actions performed on the performance obligations and lines of customer contr... |
| VRM_REVENUE_ADJUSTMENTS_ALL | TABLE | 68 | The VRM_REVENUE_ADJUSTMENTS_ALL contains all information about revenue adjustments on transactions f... |
| VRM_REVENUE_CONTINGENCIES | TABLE | 24 | The VRM_REVENUE_CONTINGENCIES contains both seeded and user-defined revenue contingency definitions. |
| VRM_REVENUE_DOCUMENTS_ALL | TABLE | 46 | VRM_REVENUE_DOCUMENTS_ALL contains source document header information that is used to create the rev... |
| VRM_REVENUE_DOCUMENT_ERRORS | TABLE | 15 | VRM_REVENUE_DOCUMENT_ERRORS table stores the errors during revenue documents processing. |
| VRM_REVENUE_DOC_LINES_ALL | TABLE | 74 | VRM_REVENUE_DOC_LINES_ALL contains all revenue lines to be recognized. |
| VRM_REVENUE_OPTIONS_ALL | TABLE | 12 | VRM_REVENUE_OPTIONS_ALL contains the processing options that are used in the revenue recognition and... |
| VRM_REVENUE_POLICIES | TABLE | 13 | VRM_REVENUE_POLICIES contains the revenue policy for revenue recognition. |
| VRM_REVENUE_RULES | TABLE | 18 | The VRM_RULES table stores invoicing and accounting rules. Receivables creates one row in this table... |
| VRM_REVENUE_RULE_SCHEDULES | TABLE | 11 | VRM_REVENUE_RULE_SCHEDULES contains revenue schedules associate to a revenue rule. |
| VRM_REVISION_LINE_AMOUNTS | TABLE | 13 | The VRM_REVISION_LINE_AMOUNTS table contains information about the amount of revenue recognized for ... |
| VRM_REV_ADJUSTMENTS_TEMP_ALL | TABLE | 34 | The VRM_REV_ADJUSTMENTS_TEMP_ALL table contains information about revenue adjustments on transaction... |
| VRM_REV_ADJ_CONTS_TEMP_ALL | TABLE | 24 | The VRM_REV_ADJ_CONTS_TEMP_ALL table contains, for each line, contingencies that impact revenue duri... |
| VRM_REV_ADJ_DEF_LNS_TEMP_ALL | TABLE | 21 | The VRM_REV_ADJ_DEF_LNS_TEMP_ALL table contains information about invoice status changes, as invoice... |
| VRM_REV_ADJ_SCHED_TEMP_ALL | TABLE | 42 | The VRM_REV_ADJ_SCHED_TEMP_ALL contains revenue schedules, which represent when and how much revenue... |
| VRM_REV_ADJ_TEMP_ALL | TABLE | 36 | The VRM_REV_ADJ_TEMP_ALL table contains information about revenue adjustments on transactions for on... |
| VRM_REV_ADJ_TEMP_SPLITS_ALL | TABLE | 27 | The VRM_REV_ADJ_TEMP_SPLITS_ALL contains revenue split information used to create revenue adjustment... |
| VRM_REV_DOC_LINE_SCHEDULES_ALL | TABLE | 55 | Revenue Schedules represent when and for how much revenue will be recognized for a given revenue lin... |
| VRM_REV_DOC_LINE_SPLITS_ALL | TABLE | 27 | VRM_REV_DOC_LINE_SPLITS_ALL contains revenue split information, which allows users to distribute rev... |
| VRM_REV_LINE_CONTS_ALL | TABLE | 31 | VRM_REV_LINE_CONTS_ALL contains revenue contingencies, per revenue document line, that impact the re... |
| VRM_SOURCE_COLUMNS_B | TABLE | 18 | VRM_SOURCE_COLUMNS_B contains the list of column names in Oracle Fusion Revenue Management applicati... |
| VRM_SOURCE_COLUMNS_TL | TABLE | 13 | VRM_SOURCE_COLUMNS_TL contains translated information for VRM_SOURCE_COLUMNS_B. |
| VRM_SOURCE_DOCUMENTS | TABLE | 195 | This object stores the documents from the upstream applications. The document lines are used for VSO... |
| VRM_SOURCE_DOC_ADDL_SUBLINES | TABLE | 51 | This table contains the fulfillment details of additional satisfaction events details of each promis... |
| VRM_SOURCE_DOC_ERRORS | TABLE | 10 | VRM_SOURCE_DOC_ERRORS contains the errors during source documents processing. |
| VRM_SOURCE_DOC_LINES | TABLE | 323 | This object stores the document lines from the upstream applications. The document lines are used fo... |
| VRM_SOURCE_DOC_SUB_LINES | TABLE | 212 | This object stores document data from the upstream applications, which is at a sub level to either d... |
| VRM_SOURCE_DOC_TYPES_B | TABLE | 22 | VRM_SOURCE_DOC_TYPES_B contains definition of document types from source applications that VRM appli... |
| VRM_SOURCE_DOC_TYPES_TL | TABLE | 14 | VRM_SOURCE_DOC_TYPES_TL contains translated information for VRM_SOURCE_DOC_TYPES_B. |
| VRM_STANDALONE_SALES | TABLE | 14 | This is an extension object to document lines that store processing results of all the processes ope... |
| VRM_SYSTEM_OPTIONS | TABLE | 33 | This object stores system level configuration options for the revenue compliance processes . |
| XCC_ACCOUNT_GROUPS | TABLE | 20 | This table stores the groups of accounts setup by each user to enable easy monitoring of funds avail... |
| XCC_ACCOUNT_GROUP_DETAILS | TABLE | 42 | This table stores the individual budget accounts that comprise each account group. This enables easy... |
| XCC_ACCT_GROUP_USER_PREFS | TABLE | 13 | This table contains user preferences for infolets display. This table includes details of budget acc... |
| XCC_BALANCES | TABLE | 26 | This table stores the budget balances and consumption of budget for each control budget, budget acco... |
| XCC_BALANCES_CUBES | TABLE | 51 | This table stores the budgetary control structure Essbase Cube information |
| XCC_BALANCE_ACTIVITIES | TABLE | 52 | This tables reflects how transactions affect the budgetary control balances. |
| XCC_BALANCE_ACTIVITIES_HISTORY | TABLE | 53 | This table stores Budgetary Control activities that have been purged from the regular XCC_BALANCE_AC... |
| XCC_BCE_BUSINESS_FUNCTIONS | TABLE | 14 | This table holds the enablement information for Budgetary Control and Encumbrance Accounting for the... |
| XCC_BCE_BUSINESS_UNITS | TABLE | 17 | This table holds the enablement information for Budgetary Control and Encumbrance Accounting for a b... |
| XCC_BCE_CASH_ACCOUNTS | TABLE | 11 | This table stores the budgetary control natural account values for the cash control budget when proc... |
| XCC_BCE_DOCUMENT_TYPES | TABLE | 12 | This table holds the enablement information for Budgetary Control and the Encumbrance Accounting for... |
| XCC_BCE_JOURNAL_CATEGORIES | TABLE | 9 | This table holds the ledger Budgetary Control enablement information for the Journal Categories. Onl... |
| XCC_BCE_JOURNAL_SOURCES | TABLE | 10 | This table holds the Journal Sources that are not enabled for a ledger. It pertains only to Budgetar... |
| XCC_BCE_LEDGERS | TABLE | 21 | This table holds the enablement information for Budgetary Control and Encumbrance Accounting for a s... |
| XCC_BCE_TRANSACTION_SOURCES | TABLE | 13 | This table holds the disablement information for Budgetary Control and the Encumbrance Accounting fo... |
| XCC_BCE_TRANSACTION_TYPES | TABLE | 13 | This table stores the customer implementation of which transaction types are enabled for budgetary c... |
| XCC_BC_BUSINESS_FUNCTIONS | TABLE | 18 | This tables stores the business functions that support budgetary control |
| XCC_BC_DISABLE_JE_SOURCES | TABLE | 11 | This table contains journal sources that are disabled by default. You can enable those journal sourc... |
| XCC_BC_SOURCE_DEFINITIONS | TABLE | 30 | This table stores the configuration of how transaction types, actions affect budgetary control balan... |
| XCC_BC_TRANSACTION_SUBTYPES | TABLE | 14 | This table stores the transaction types and subtypes enabled for budgetary control. |
| XCC_BC_TRANSACTION_TYPES | TABLE | 13 | This table stores details of the available transaction types |
| XCC_BC_TR_REPROCESS_LINES | TABLE | 11 | This table contains transactions that previously failed budgetary control and are reprocessed during... |
| XCC_BUDGET_ACCOUNTS | TABLE | 43 | This table contains all combinations of budget chart of accounts associated to control budgets. The ... |
| XCC_BUDGET_DIST_ACCTS | TABLE | 18 | This table stores budget amount per control budget, budget account and period. |
| XCC_BUDGET_DIST_ACCTS_HISTORY | TABLE | 19 | This table contains budget distribution accounts that have been purged from the standard XCC_BUDGET_... |
| XCC_BUDGET_DIST_HDRS_HISTORY | TABLE | 19 | This table contains budget distribution headers that have been purged from the standard XCC_BUDGET_D... |
| XCC_BUDGET_DIST_HEADERS | TABLE | 25 | This table strores the budget distribution headers during budget import. |
| XCC_BUDGET_DIST_LINES | TABLE | 55 | This table stores the distribution line information of budget initialization and adjustments |
| XCC_BUDGET_DIST_LINES_HISTORY | TABLE | 53 | This table contains budget distribution lines that have been purged from the standard XCC_BUDGET_DIS... |
| XCC_CB_COMPILED_RULES | TABLE | 10 | This table is for internal processing by the budgetary control engine and contains the control budge... |
| XCC_CB_FLAT_SEGMENTS | TABLE | 123 | This table contains the control bubdget key segments in a flat format for easier control and process... |
| XCC_CB_KEY_SEGMENTS | TABLE | 15 | This table stores the control budget account segments and thier mappings to either accounting flex f... |
| XCC_CB_KEY_SEG_TREE_VERSIONS | TABLE | 20 | This table stores the tree label and tree versions assigned to a control budget key segment over dif... |
| XCC_CB_OVERRIDE_COMPILED | TABLE | 13 | This table contains compiled override information, in a format that is easier to use by the budgetar... |
| XCC_CB_OVERRIDE_JOURNALS | TABLE | 11 | This table contains the journal sources and categories for which an override rule is applicable. It ... |
| XCC_CB_OVERRIDE_RULES | TABLE | 16 | This table contains the override rules for a control budget. It stores both insufficient funds overr... |
| XCC_CB_OVERRIDE_TRANS_TYPES | TABLE | 10 | This table contains the transaction types for which an override rule applies. It does not contain an... |
| XCC_CB_OVERRIDE_USERS | TABLE | 10 | This table contains details of the users that an override rule has been assigned to. |
| XCC_CB_PERIOD_STATUSES | TABLE | 22 | This table stores the periods statuses for control budgets which control when budget is available fo... |
| XCC_CB_RULES | TABLE | 24 | This table stores the implemented control budget supplementary rules and revenue funding rules. |
| XCC_CB_RULE_FILTER_CONDITIONS | TABLE | 14 | This table stores all the supplemental rule filters. These filters can be based on budget segments, ... |
| XCC_CB_RULE_FILTER_COND_VALS | TABLE | 10 | This table stores the rule filter condition values for supplementary rules and revenue funding rules... |
| XCC_CB_SUMRY_PERIOD_MAPPINGS | TABLE | 10 | This table stores the period mapping for related control budgets. The child control budget period is... |
| XCC_CF_TRANSACTIONS | TABLE | 16 | This table contains purchase orders processed by the carry forward enterprise service scheduler proc... |
| XCC_CF_TRANSACTION_ERRORS | TABLE | 12 | This table contains any errors encountered by the carry forward enterprise service scheduler process... |
| XCC_CONTROL_BUDGETS | TABLE | 59 | This table stores the header information for a control budget. |
| XCC_CONTROL_BUDGET_ERRORS | TABLE | 24 | This table stores the processing errors encountered during the control budget creation. |
| XCC_CUBE_TREE_VERSIONS | TABLE | 11 | This table contains the tree versions stored in budgetary control essbase cubes. It also contains th... |
| XCC_DATA_SETS | TABLE | 22 | The table contains a row for each call to the budgetary control engine. It contains the parameters t... |
| XCC_ESSBASE_BAL_ROWS | TABLE | 7 | This table contains the transaction rows for a refresh balances run. |
| XCC_ESSBASE_DATA_RUNS | TABLE | 15 | This table stores all the submitted ESS jobs and specific data runs for the updating the budgetary c... |
| XCC_ESSBASE_DUPLICATE_PARENTS | TABLE | 12 | Table to store duplicate member info at parent level within the incoming tree versions compared to t... |
| XCC_ESSBASE_REPORTING_TREES | TABLE | 11 | This table contains the tree versions copied to Oracle Fusion Budgetary Control Essbase cubes solely... |
| XCC_MASTER_PROCESSES | TABLE | 7 | XCC_MASTER_PROCESSES stores the status of the balance streaming master process. |
| XCC_PENDING_ACTIVITIES | TABLE | 89 | This tables stores the impact of the XCC transaction lines on the budget balances for in process tra... |
| XCC_PROCESS_ERRORS | TABLE | 18 | This table stores the processing errors encountered during the budget import program. |
| XCC_RECALC_PROCESS_ERRORS | TABLE | 20 | This table contains all the errors encountered during recalculation. |
| XCC_REFRESH_TREE_HISTORY | TABLE | 13 | This table contains the control budgets and tree versions impacted by the Refresh Tree for Budgetary... |
| XCC_REV_FUND_REQUESTS | TABLE | 19 | This table contains a record for each create expense budget entry from revenue enterprise service sc... |
| XCC_REV_FUND_REQUEST_RULES | TABLE | 24 | This table contains a record for each control budget and revenue funding rule processed by the creat... |
| XCC_REV_FUND_REQ_RULE_SOURCES | TABLE | 10 | This table contains a record of each revenue funding rule and revenue source account combination amo... |
| XCC_REV_FUND_REQ_RULE_TARGETS | TABLE | 9 | This table contains a record of each revenue funding rule and funding target account combination amo... |
| XCC_REV_FUND_RULE_BALANCES | TABLE | 9 | This tables stores the budget balance funded from revenue by control budget, revenue funding rule an... |
| XCC_SEG_NOT_BUDGETED_SEG_VAL | TABLE | 11 | This table contains a filler segment value for any segment in a ledger's chart of accounts that is e... |
| XCC_SEG_VAL_HIER_RF | TABLE | 28 | This table contains the relationship between various nodes in a given tree version in row-flattened ... |
| XCC_SEG_VAL_HIER_SNAPSHOT | TABLE | 29 | This table is used by the refresh tree for budgetary control process to keep a snapshot of the row-f... |
| XCC_SIM_HEADERS | TABLE | 20 | Stores transaction information for a pseudo application used for testing the budgetary control engin... |
| XCC_SIM_LINES | TABLE | 68 | Stores transaction line information for a pseudo application used for testing the budgetary control ... |
| XCC_SL_TR_HEADERS | TABLE | 11 | This table stores the details of subledger transactions that have been involved in an override actio... |
| XCC_SL_TR_NOTIFICATIONS | TABLE | 13 | This table stores details for override notifications. It stores the list of overriders to whom notif... |
| XCC_SL_TR_OVERRIDERS | TABLE | 11 | This table stores users that can override a subledger or general ledger transaction. This table only... |
| XCC_STREAM_BALANCES_T | TABLE | 9 | This temporary table contains budgetary control balances impacted by budget imports and transactions... |
| XCC_SYSTEM_OPTIONS | TABLE | 9 | This table contains enterprise level feature settings for Budgetary Control and Encumbrance Accounti... |
| XCC_TREE_VERSIONS | TABLE | 13 | This table contains the tree versions that are extracted into budgetary control. It also contains th... |
| XCC_TR_BALANCES | TABLE | 28 | This table temporarily stores the balance updates for each budgetary control validation request unti... |
| XCC_TR_HEADERS | TABLE | 30 | This table stores the transaction header attributes calling the budgetary control engine. There are ... |
| XCC_TR_HEADERS_HISTORY | TABLE | 30 | This table contains budgetary control transactions that have been purged from the regular XCC_TR_HEA... |
| XCC_TR_LINES | TABLE | 82 | This table stores the transaction lines associated with each commitment control transaction. It stor... |
| XCC_TR_LINES_HISTORY | TABLE | 82 | This table contains budgetary control transaction lines that have been purged from the regular XCC_T... |
| XLA_ACCOUNTING_ERRORS | TABLE | 22 | This table contains the errors encountered during execution of the Accounting Program. |
| XLA_ACCTG_METHODS_B | TABLE | 14 | This table contains Subledger Accounting Methods across products. Subledger Accounting Methods provi... |
| XLA_ACCTG_METHODS_TL | TABLE | 15 | This table contains translated information about Subledger Accounting Methods. |
| XLA_ACCTG_METHOD_RULES | TABLE | 18 | This is a date effective table that stores the Accounting Method to Product Rule. |
| XLA_ACCT_ATTRIBUTES_B | TABLE | 19 | This table contains accounting attributes. |
| XLA_ACCT_ATTRIBUTES_TL | TABLE | 13 | This table captures translated values for the accounting attributes. Accounting attributes are prede... |
| XLA_ACCT_CLASS_ASSGNS | TABLE | 15 | This table contains the accounting class assignments for the Post-Accounting Programs. |
| XLA_ACCT_LINE_TYPES_B | TABLE | 32 | This table stores journal line rules. |
| XLA_ACCT_LINE_TYPES_TL | TABLE | 19 | This table contains translated information about Journal Line Rules. |
| XLA_ACCT_RULE_DEFINITIONS | TABLE | 10 | This table contains Accounting Rule Defintions as a CLOB object in the database. |
| XLA_AC_BALANCES | TABLE | 69 | This table contains supporting reference balances. |
| XLA_AE_HEADERS | TABLE | 65 | This table contains subledger accounting journal entries. |
| XLA_AE_HEADER_ACS | TABLE | 15 | This table contains the supporting references segment values for a journal entry header. |
| XLA_AE_LINES | TABLE | 127 | This table contains the journal entry lines for each subledger accounting journal entry. |
| XLA_AE_LINE_ACS | TABLE | 16 | This table contains the segment values for supporting references assigned to a journal entry line. |
| XLA_AE_SEGMENT_VALUES | TABLE | 14 | This table contains information about the balancing or management segment values associated with the... |
| XLA_AMB_SETUP_ERRORS | TABLE | 44 | This table contains errors reported by the Create and Assign Source program and the Activate Journal... |
| XLA_ANALYTICAL_DTLS_B | TABLE | 13 | This table contains the translated header information (name and description) for the Analytical Crit... |
| XLA_ANALYTICAL_DTLS_TL | TABLE | 14 | This table contains the translations for the supporting references details. |
| XLA_ANALYTICAL_HDRS_B | TABLE | 24 | This table contains the header information for the analytical criteria. Since some analytical criter... |
| XLA_ANALYTICAL_HDRS_TL | TABLE | 16 | This table contains the translated header information (name and description) for Supporting Referenc... |
| XLA_ANALYTICAL_SOURCES | TABLE | 20 | This table contains the sources for the supporting references. |
| XLA_ASSIGNMENT_DEFNS_B | TABLE | 16 | This table contains the ledger assignments for the Post-Accounting Programs. |
| XLA_ASSIGNMENT_DEFNS_TL | TABLE | 16 | This table contains the translated columns for accounting class ledger assignments. |
| XLA_BALANCE_STATUSES | TABLE | 23 | This table contains the status of the balance for a code combination identifier and allows the simul... |
| XLA_BAL_CONCURRENCY_CONTROL | TABLE | 6 | Use internally for balance calculation program concurrency control. |
| XLA_CONDITIONS | TABLE | 36 | This table contains the conditions for journal line rules, account rules and description rules. |
| XLA_CONFIGURATION_VALUES | TABLE | 26 | This table contains a record of all the Oracle Fusion Subledger Accounting configuration values. |
| XLA_CONTROL_BALANCES | TABLE | 29 | This table contains the third party control balances. |
| XLA_DATA_FILES | TABLE | 27 | This table contains interim copies of data files uploaded into or extracted from Oracle Financial Ac... |
| XLA_DESCRIPTIONS_B | TABLE | 16 | This table contains all description rules created for an application. |
| XLA_DESCRIPTIONS_TL | TABLE | 17 | This table contains translated information about the descriptions. |
| XLA_DESCRIPT_DETAILS_B | TABLE | 20 | This table contains the details of a description. It holds a string of literal and sources in the se... |
| XLA_DESCRIPT_DETAILS_TL | TABLE | 14 | This table contains the translation details of description rules. |
| XLA_DESC_PRIORITIES | TABLE | 15 | This table contains priority information about descriptions. |
| XLA_DIAG_EVENTS | TABLE | 18 | This table contains the information relative to the events processed by the diagnostic framework. |
| XLA_DIAG_LEDGERS | TABLE | 22 | This table contains the information related to the ledgers used by the accounting program to create ... |
| XLA_DIAG_SOURCES | TABLE | 22 | This table is used to contain the source values retrieved from the transaction objects by the Diagno... |
| XLA_DISTRIBUTION_LINKS | TABLE | 99 | This table contains the link between transactions and subledger journal entry lines. |
| XLA_ENTITY_ID_MAPPINGS | TABLE | 19 | This table contains the mapping of the primary key columns of the entity table of the event table. I... |
| XLA_ENTITY_TYPES_B | TABLE | 13 | This table contains all event entities that are used to group event classes. |
| XLA_ENTITY_TYPES_TL | TABLE | 15 | This table contains translated information related to entity. |
| XLA_EVENTS | TABLE | 43 | This table contains all information related to a specific event. This table is created as a type XLA... |
| XLA_EVENTS_OAR | TABLE | 12 | Events inside of an online accounting request. |
| XLA_EVENT_CLASSES_B | TABLE | 13 | This table contains all event classes for an entity. |
| XLA_EVENT_CLASSES_TL | TABLE | 16 | This table contains translated information related to event classes. |
| XLA_EVENT_CLASS_ATTRS | TABLE | 22 | This table contains detailed information related to event classes. |
| XLA_EVENT_CLASS_GRPS_B | TABLE | 12 | This table contains process categories. |
| XLA_EVENT_CLASS_GRPS_TL | TABLE | 15 | This table contains translated information about process categories. |
| XLA_EVENT_CLASS_ORDER | TABLE | 14 | This table contains the event classes processing order for a particular application. The data in thi... |
| XLA_EVENT_CLASS_PREDECS | TABLE | 13 | This table contains the predecessors of the event classes. |
| XLA_EVENT_MAPPINGS_B | TABLE | 15 | This table contains information to build reports based on information available on the base document... |
| XLA_EVENT_MAPPINGS_TL | TABLE | 13 | This table contains translated information related to event mappings. |
| XLA_EVENT_SOURCES | TABLE | 21 | This table connects sources and event classes. |
| XLA_EVENT_TYPES_B | TABLE | 17 | This table contains all event types that belong to an event class. |
| XLA_EVENT_TYPES_TL | TABLE | 17 | This table contains translated information about event types. |
| XLA_EVENT_TYPE_SOURCES | TABLE | 31 | This table contains sources used by an event type in context of the application accounting definitio... |
| XLA_EVT_CLASS_ACCT_ATTRS | TABLE | 19 | This table contains standard, system, and custom sources assigned to an accounting attribute at the ... |
| XLA_EXTERNAL_SYSTEM_LEDGER_MAP | TABLE | 10 | This table contains mapping between the Oracle Fusion General Ledger and external transaction ledger... |
| XLA_EXTRACT_OBJECTS | TABLE | 16 | This table contains the extract object name and type used by the Accounting Program to derive source... |
| XLA_FORMULAS_B | TABLE | 20 | This table contains subledger formulas. |
| XLA_FORMULAS_TL | TABLE | 14 | This table contains translated information for subledger formulas. |
| XLA_FORMULA_DETAILS | TABLE | 14 | This table contains the detail expression of a subledger formula. |
| XLA_FORMULA_FUNCTIONS_B | TABLE | 25 | This table contains predefined functions which can be used in subledger formulas. |
| XLA_FORMULA_FUNCTIONS_TL | TABLE | 24 | This table contains translated information of predefined functions that can be used in subledger for... |
| XLA_FORMULA_SOURCES | TABLE | 16 | This table contains all sources used in a subledger formula. |
| XLA_INTERNAL_PROCESSING_TASKS | TABLE | 27 | This table contains a record of all the Oracle Fusion Subledger Accounting maintenance tasks run in ... |
| XLA_JERS_AAD_ASSGNS | TABLE | 17 | This table contains the assignments of the product rule to journal entry rule set. |
| XLA_JERS_ADR_LINES | TABLE | 24 | This table contains the assignments of the account rules to the journal line rule in a journal entry... |
| XLA_JERS_ATTRS_ASSGNS | TABLE | 21 | This table contains the assignments between journal entry rule set and the accounting attributes at ... |
| XLA_JERS_COMPILED_METADATA | TABLE | 17 | This table contains the compiled status, locking status, and accounting rule definition for each edi... |
| XLA_JERS_INHERITED | TABLE | 17 | This table contains the relationship between the journal entry rule set in the context and the relat... |
| XLA_JERS_JLT_LINES | TABLE | 27 | This table contains the assignments of the journal line rules and description rules to a journal ent... |
| XLA_JERS_SR_HDR_ASSGNS | TABLE | 18 | This table contains assignment of header level suppporting reference to a journal entry rule set. |
| XLA_JERS_SR_LINE_ASSGNS | TABLE | 20 | This table contains line level assignment of supporting references to a journal entry rule set. |
| XLA_JE_CATEGORIES | TABLE | 12 | This table contains Journal Categories for a combination of an event class and an application. |
| XLA_JE_RULE_SETS_B | TABLE | 26 | This table contains the journal entry rule set information. |
| XLA_JE_RULE_SETS_TL | TABLE | 19 | This table contains translation for XLA_JE_RULE_SETS_B. |
| XLA_JLT_ACCT_ATTRS | TABLE | 20 | This table contains sources assigned to accounting attributes for the Journal Line Rules. |
| XLA_LAUNCH_OPTIONS | TABLE | 21 | This table contains the default values for accounting program launch options for an application and ... |
| XLA_LEDGER_OPTIONS | TABLE | 21 | This table contains the subledger accounting options. |
| XLA_MAPPING_SETS_B | TABLE | 21 | This table contains the mapping set header definition. |
| XLA_MAPPING_SETS_TL | TABLE | 16 | This table contains the header information of a mapping set definition. |
| XLA_MAPPING_SET_FLAVORS | TABLE | 15 | This table contains chart of accounts or value sets assigned to mapping sets. |
| XLA_MAPPING_SET_INPUTS | TABLE | 22 | This table stores the Mapping set input sources and the overridden information. The source_code, sou... |
| XLA_MAPPING_SET_VALUES | TABLE | 31 | This table contains output values map to each combination of input values for a mapping set. |
| XLA_MERGE_SEG_MAPS | TABLE | 16 | This table contains the segment mapping for third party merge. |
| XLA_MPA_DISTRIBUTIONS | TABLE | 43 | This table keeps track the MPA accounting progress and the running recognized amounts for an event, ... |
| XLA_MPA_HEADER_AC_ASSGNS | TABLE | 16 | This table contains the multiperiod journal lines assigned to the accrual journal line types in a jo... |
| XLA_MPA_JLT_AC_ASSGNS | TABLE | 19 | This table contains the analytical criteria assigned to multiperiod journal lines for accrual journa... |
| XLA_MPA_JLT_ADR_ASSGNS | TABLE | 21 | This table contains the account derivation rules assigned to multiperiod journal lines for accrual j... |
| XLA_MPA_JLT_ASSGNS | TABLE | 19 | This table contains the multiperiod journal lines assigned to the accrual journal line types in a jo... |
| XLA_ONLINE_ACCTING_REQS | TABLE | 18 | This table contains Online Accounting Requests. |
| XLA_ONLINE_TXN_ENGINES | TABLE | 18 | This table contains the definition of the transaction engines. |
| XLA_ONLINE_TXN_PROCS | TABLE | 18 | This table represents the collection of processes running the online transaction engine. Each row wi... |
| XLA_OTE_TEST | TABLE | 9 | This table contains online accounting engine related data. |
| XLA_PARTIAL_MERGE_TXNS | TABLE | 22 | This table contains the transactions for a partial third party merge. The partial third party merge ... |
| XLA_POST_ACCT_PROGS_B | TABLE | 12 | This table contains the post-accounting programs. |
| XLA_POST_ACCT_PROGS_TL | TABLE | 15 | This table contains the translated columns for the Post-Accounting Programs. |
| XLA_PRODUCT_RULES_B | TABLE | 25 | This table contains the accounting rules for an application. Standard product accounting rules are i... |
| XLA_PRODUCT_RULES_TL | TABLE | 17 | This table contains translated information about application accounting definitions. |
| XLA_PROD_ACCT_HEADERS | TABLE | 25 | This table optionally contains the accounting headers types for a Application Accounting Definition ... |
| XLA_REFERENCE_OBJECTS | TABLE | 20 | This table contains reference objects associated with transaction objects of event classes. |
| XLA_SEG_RULES_B | TABLE | 22 | This table contains for all account rules. |
| XLA_SEG_RULES_TL | TABLE | 17 | This table contains translated information of account rule. |
| XLA_SEG_RULE_DETAILS | TABLE | 32 | This table contains the account rule details information. |
| XLA_SELF_CORRECTIONS | TABLE | 43 | This backup table stores records updated by the self correction process. |
| XLA_SLAM_JE_RULE_SETS | TABLE | 21 | This table contains the journal entry rule set assignment to accounting methods. |
| XLA_SOURCES_B | TABLE | 32 | This table contains all subledger sources and sources customized by the user. These sources are used... |
| XLA_SOURCES_TL | TABLE | 16 | This table contains translated information about sources. |
| XLA_SOURCE_PARAMS | TABLE | 16 | This table contains all parameters used in the PL/SQL function for a user-defined source. |
| XLA_SRC_TRX_SPLIT_DETAILS | TABLE | 18 | This table contains the association between the Accounting Hub transaction data file, original trans... |
| XLA_SRC_TRX_SUMMARIZED_DETAILS | TABLE | 159 | This table contains the association between the Accounting Hub transaction data file, original line ... |
| XLA_SUBLEDGERS | TABLE | 28 | Fusion Subledger Application Table. FND_APPLICATION_VL is replaced by this table. |
| XLA_SUBLEDGERS_TL | TABLE | 14 | This table contains translatable information about subledger Application registered in Oracle Fusion... |
| XLA_SUPP_REF_VALUES_ESSBASE | TABLE | 8 | This table contains unique values to populate ESSBASE members. |
| XLA_SUP_REF_COMBINATIONS | TABLE | 66 | This table contains unique supporting reference combination. |
| XLA_TAB_ACCT_DEFS_B | TABLE | 19 | This table contains all transaction account definitions. |
| XLA_TAB_ACCT_DEFS_TL | TABLE | 17 | This table contains the translations for the transaction account definition. |
| XLA_TAB_ACCT_DEF_DETAILS | TABLE | 18 | This table contains the assignment of Transaction Account Types and Account Derivation Rules to Tran... |
| XLA_TAB_ACCT_TYPES_B | TABLE | 15 | This table contains all Transaction Account Types. |
| XLA_TAB_ACCT_TYPES_TL | TABLE | 15 | This table contains the translations for the Transaction Account Builder account types. |
| XLA_TAB_ACCT_TYPE_SRCS | TABLE | 14 | This table contains all transaction account type sources. |
| XLA_TAB_COMPILED_METADATA | TABLE | 13 | This table contains the compiled status for each edition of the transaction account definition. |
| XLA_TAB_SETUP_ERRORS | TABLE | 17 | This table contains errors generated by the Transaction Account Definitions Activation program. The ... |
| XLA_TPM_WORKING_HDRS_T | TABLE | 6 | This table is used by the Third Party Merge PL/SQL. |
| XLA_TRANSACTION_CONTROL_DETAIL | TABLE | 10 | This table stores information about dynamic interface tables created for each event class imported i... |
| XLA_TRANSACTION_ENTITIES | TABLE | 34 | This table contains a row for each transaction for which events have been raised in Subledger Accoun... |
| XLA_TRANSACTION_HEADERS | TABLE | 98 | This table contains Oracle Fusion Accounting Hub transaction data for use in accounting. |
| XLA_TRANSACTION_LINES | TABLE | 164 | This table contains Oracle Fusion Accounting Hub transaction line data for use in accounting. |
| XLA_TRANSFER_LEDGERS | TABLE | 12 | This table contains secondary ledgers processed by the transfer to General Ledger batch. |
| XLA_TRANSFER_LOGS | TABLE | 15 | This table contains the transfer to General Ledger log information. This information is used to reco... |
| XLE_ASSOCIATIONS | TABLE | 35 | XLE_ASSOCIATIONS contains the legal associations. |
| XLE_ASSOCIATION_TYPES | TABLE | 16 | XLE_ASSOCIATION_TYPES contains the different association types that will be used in legal associatio... |
| XLE_ASSOC_OBJECT_TYPES | TABLE | 15 | XLE_ASSOC_OBJECT_TYPES contains the different object types that will be used in legal associations. |
| XLE_CONTACT_LEGAL_ROLES | TABLE | 16 | XLE_CONTACT_LEGAL_ROLES contains the legal roles that a contact can have. |
| XLE_ENTITY_PROFILES | TABLE | 52 | XLE_ENTITY_PROFILES contains the general information, which identifies a party with the classificati... |
| XLE_ETB_PROFILES | TABLE | 51 | XLE_ETB_PROFILES contains the general information, which identifies a Party (HZ_PARTIES) with the cl... |
| XLE_HISTORIES | TABLE | 15 | XLE_HISTORIES contains table and column names for tracked Registration attributes. |
| XLE_HISTORY_COLUMNS_B | TABLE | 10 | XLE_HISTORY_COLUMNS_B contains the information about tracked legal entity and establishment attribut... |
| XLE_HISTORY_COLUMNS_TL | TABLE | 10 | XLE_HISTORY_COLUMNS_TL contains the translations of the prompts for tracked legal entity and establi... |
| XLE_JURISDICTIONS_B | TABLE | 21 | XLE_JURISDICTIONS contains the information about Jurisdictions. |
| XLE_JURISDICTIONS_TL | TABLE | 13 | XLE_JURISDICTIONS_TL contains the translations of the prompts for Jurisdictions. |
| XLE_JUR_FUNCTIONS | TABLE | 11 | XLE_JUR_FUNCTIONS contains the legal functions that the legal entity or establishment might have to ... |
| XLE_REGISTRATIONS | TABLE | 42 | XLE_REGISTRATIONS contains the detailed registration information of legal entities and establishment... |
| XLE_REG_FUNCTIONS | TABLE | 12 | XLE_REG_FUNCTIONS contains the legal functions that a legal entity or an establishment should perfor... |
| ZX_ACCOUNTS | TABLE | 30 | This table contains default tax accounts for jurisdictions and rates which capture the financial imp... |
| ZX_ACCOUNT_RATES | TABLE | 24 | This table stores Tax Account Rate information |
| ZX_ACCT_TX_CLS_DEFS_ALL | TABLE | 12 | This table stores tax classification code defaults for account segment values |
| ZX_API_CODE_COMBINATIONS | TABLE | 28 | This table stores valid context combinations for each context key flexfield structure, using third p... |
| ZX_API_OWNER_STATUSES | TABLE | 8 | This table stores the status of APIs registration for an API owner |
| ZX_API_REGISTRATIONS | TABLE | 17 | This table stores registrations of APIs required to support third party tax service providers. Each ... |
| ZX_AR_COND_ACTIONS_ALL | TABLE | 13 | The AR_TAX_CONDITION_ACTIONS_ALL table stores actions for each tax condition that you define in the ... |
| ZX_AR_LOCATION_VALUES_OLD | TABLE | 29 | The AR_LOCATION_VALUES table defines each jurisdiction that Oracle Receivables uses to validate segm... |
| ZX_AR_LOCN_ACCOUNTS_ALL | TABLE | 23 | The AR_LOCATION_ACCOUNTS_ALL table stores tax accounting information for all records in the AR_LOCAT... |
| ZX_AR_TAX_CONDITIONS_ALL | TABLE | 10 | The AR_TAX_CONDITIONS_ALL table stores information about tax condition sets, which are user-defined ... |
| ZX_AR_TAX_COND_LINES_ALL | TABLE | 15 | The AR_TAX_CONDITION_LINES_ALL table stores the expression lines that define a tax condition. Each e... |
| ZX_BUCKETS_F | TABLE | 32 | This table stores detail information about tax to date amount and taxable to date amount buckets ass... |
| ZX_COMPOUND_ERRORS | TABLE | 11 | This table stores errors found during tax groups migration from ZX_TAX_PRIORITIES_T. |
| ZX_COMPOUND_ERRORS_T | TABLE | 13 | This temporary table stores errors found during tax groups migration from ZX_TAX_PRIORITIES_T. |
| ZX_CONDITIONS | TABLE | 27 | This table stores Tax Conditions |
| ZX_CONDITION_DETAILS | TABLE | 24 | This table stores Tax Condition Details |
| ZX_CONDITION_GROUPS_B | TABLE | 131 | This table stores Condition Groups |
| ZX_CONDITION_GROUPS_TL | TABLE | 10 | This table provides multilingual support (MLS) for each tax condition set. MLS enables you to store ... |
| ZX_CONTENT_CHOICES_TMP | TABLE | 8 | This is a temporary table which is used internally by Oracle. |
| ZX_CONTENT_SOURCES | TABLE | 21 | This table stores Tax Content Providers |
| ZX_DATA_UPLOAD_DISCARD | TABLE | 43 | This is an intermediate table used by the data upload program to temporarily hold the content from t... |
| ZX_DEFAULTING_RULE_RESULTS_F | TABLE | 105 | This table contains tax rules that are defined to evaluate the default values of the tax determinant... |
| ZX_DETERMINING_FACTORS_B | TABLE | 30 | This table stores Tax Determining Factors |
| ZX_DET_DEFAULT_MAPPING_F | TABLE | 19 | ZX_DET_DEFAULT_MAPPING_F contains mappings for defaulting tax determinants. |
| ZX_DET_FACTORS_TL | TABLE | 13 | This table provides multilingual support (MLS) for each determining factor. MLS enables you to store... |
| ZX_DET_FACTOR_TEMPL_B | TABLE | 22 | This table stores the sets of determining factors. Each record represents one determining factor set... |
| ZX_DET_FACTOR_TEMPL_DTL | TABLE | 22 | This table stores a set of determining factors for each determining factor set defined in ZX_DET_FAC... |
| ZX_DET_FACTOR_TEMPL_TL | TABLE | 13 | This table provides multilingual support (MLS) for each determining factor set. MLS enables you to s... |
| ZX_DIST_TAX_BOX_ASSGNMNTS | TABLE | 25 | This table stores the tax box assignment for a given tax line or distribution. |
| ZX_EVENT_CLASSES_B | TABLE | 11 | This table stores tax event classes, which are business classifications used to categorize a group o... |
| ZX_EVENT_CLASSES_TL | TABLE | 12 | This table provides multilingual support (MLS) for each tax event class. MLS enables you to store an... |
| ZX_EVENT_CLASS_PARAMS | TABLE | 10 | This table stores the list of parameters not passed by applications |
| ZX_EVNT_CLS_MAPPINGS | TABLE | 101 | This table stores mappings of tax event classes to application event classes of Oracle Applications. |
| ZX_EVNT_CLS_OPTIONS | TABLE | 54 | This table stores tax options for application event classes. Each row contains tax options defined b... |
| ZX_EVNT_CLS_TYPS | TABLE | 11 | This table stores tax event types, which are actions on a tax event class, which results in a call t... |
| ZX_EVNT_TYP_MAPPINGS | TABLE | 17 | This table stores Tax Event Type Mappings |
| ZX_EXCEPTIONS | TABLE | 35 | This table stores tax rate exceptions for items and product fiscal classifications, which are condit... |
| ZX_EXEMPTIONS | TABLE | 47 | This table stores tax exemptions, which are full or partial exclusions from taxes within a given tim... |
| ZX_FC_CODES_B | TABLE | 24 | This table stores fiscal classification codes, which are classifications used by tax authorities. Ea... |
| ZX_FC_CODES_CATEG_ASSOC | TABLE | 18 | This table stores the association of the classification codes of transaction fiscal classification c... |
| ZX_FC_CODES_DENORM_B | TABLE | 38 | This table stores denormalized FC Codes |
| ZX_FC_CODES_DENORM_TL | TABLE | 26 | Translate table for ZX_FC_CODES_DENORM_B base table |
| ZX_FC_CODES_TL | TABLE | 12 | This table provides multilingual support (MLS) for each fiscal classification code. MLS enables you ... |
| ZX_FC_COUNTRY_DEFAULTS | TABLE | 35 | This table stores tax defaults and controls for multiple countries. Each record contains tax default... |
| ZX_FC_TYPES_B | TABLE | 28 | This table stores fiscal classification types, which are the schemes or systems of classification or... |
| ZX_FC_TYPES_REG_ASSOC | TABLE | 17 | This table stores the association of fiscal classification types to multiple tax regimes. Each row s... |
| ZX_FC_TYPES_TL | TABLE | 12 | This table provides multilingual support (MLS) for each fiscal classification type. MLS enables you ... |
| ZX_FINAL_DISCHARGE_LOCATIONS | TABLE | 11 | Stores information associated with the final destination location for the purchases made by a custom... |
| ZX_FORMULA_B | TABLE | 35 | This table stores tax formulas that will be used to calculate taxable basis and tax amounts. Each ro... |
| ZX_FORMULA_DETAILS | TABLE | 18 | Tax Formula Details is a child table of Tax Formula |
| ZX_FORMULA_TL | TABLE | 13 | This table provides multilingual support (MLS) for each tax formula. MLS enables you to store and pr... |
| ZX_ID_TCC_MAPPING_ALL | TABLE | 21 | This table stores the list of tax classification codes applicable for an internal organization. This... |
| ZX_IMPORT_ERRORS | TABLE | 24 | This table stores processing or validation errors. This would help the user to review the errors and... |
| ZX_ITEM_DISTRIBUTIONS | TABLE | 117 | This table stores the item distributions information for the external transaction. |
| ZX_JURISDICTIONS_B | TABLE | 33 | This table stores Tax Jurisdiction information |
| ZX_JURISDICTIONS_TL | TABLE | 9 | This table is a TL table for ZX_JURISDICTIONS_B |
| ZX_LINES | TABLE | 292 | This table stores detail tax lines for transactions of multiple event classes. |
| ZX_LINES_DET_FACTORS | TABLE | 402 | This table stores Lines Determing Factors |
| ZX_LINES_SUMMARY | TABLE | 111 | This table stores the summary tax lines for transactions of multiple event classes. |
| ZX_PARAMETERS_B | TABLE | 16 | This table stores the definitions of all tax parameters, which are used in published tax services of... |
| ZX_PARAMETERS_TL | TABLE | 12 | This table provides multilingual support (MLS) for each tax parameter. MLS enables you to store and ... |
| ZX_PARAM_DETAILS | TABLE | 12 | This table stores the elements for structured tax parameters. |
| ZX_PARTY_DEDUCTIONS_F | TABLE | 18 | This table stores information about tax deductions such as social security, alimony, etc for a parti... |
| ZX_PARTY_TAXPAYER_IDNTFS | TABLE | 15 | This table contains taxpayer identifier information related to party such as supplier or customer. |
| ZX_PARTY_TAX_PROFILE | TABLE | 54 | This table stores Party Tax Profile Information |
| ZX_PARTY_TYPES | TABLE | 15 | This table stores party types, which are classifications used to categorize a party. |
| ZX_PO_REC_DIST | TABLE | 10 | This table stores the calculated recovery rate for purchase order tax lines and distributions migrat... |
| ZX_PROCESS_RESULTS | TABLE | 43 | This table stores the results from the evaluation for tax rules. Each record stores the process resu... |
| ZX_PROCESS_RESULT_DETAILS | TABLE | 16 | This table stores details assocaited with the rule process result. |
| ZX_PRODUCT_OPTIONS_ALL | TABLE | 34 | This table stores the tax system options for multiple applications. Each record stores tax options o... |
| ZX_QUICK_RULE_RESULTS_F | TABLE | 71 | This table contains tax rules that are defined to evaluate the rule results based on the tax determi... |
| ZX_RATES_B | TABLE | 49 | This table stores tax rates and the related attributes for multiple configuration owners. Each row s... |
| ZX_RATES_TL | TABLE | 10 | This table provides multilingual support (MLS) for each tax rate. MLS enables you to store and print... |
| ZX_RATE_SCHEDULES_F | TABLE | 14 | This table contains information about tax rate schedules. |
| ZX_RECOVERY_TYPES_B | TABLE | 17 | This table stores the recovery types, which classify the full or partial reclaim of taxes paid on th... |
| ZX_RECOVERY_TYPES_TL | TABLE | 10 | This table provides multilingual support (MLS) for each recovery type. MLS enables you to store and ... |
| ZX_REC_NREC_DIST | TABLE | 165 | This table stores tax distributions for tax lines on an invoice. Each record stores a recoverable or... |
| ZX_REGIMES_B | TABLE | 70 | This table stores tax regimes and the related attributes. There will be one row per distinct tax reg... |
| ZX_REGIMES_TL | TABLE | 9 | This table provides multilingual support (MLS) for each tax regime. MLS enables you to store and pri... |
| ZX_REGIMES_USAGES | TABLE | 11 | This table stores the list of regimes for each first party organization, where the transactions of t... |
| ZX_REGIME_RELATIONS | TABLE | 17 | This table stores Regime Hierarchy information |
| ZX_REGISTRATIONS | TABLE | 54 | This table stores tax registrations, which are registrations of a party with a tax authority that co... |
| ZX_REPORTING_CODES_B | TABLE | 24 | This table stores the tax reporting codes, which are unique codes for tax reporting purposes. |
| ZX_REPORTING_CODES_TL | TABLE | 12 | This is a TL table for ZX_REPORTING_CODES_B |
| ZX_REPORTING_TYPES_B | TABLE | 32 | This table stores the tax reporting types, which identify specific units of information, such as a d... |
| ZX_REPORTING_TYPES_TL | TABLE | 12 | This tables is a TL for ZX_REPORTING_TYPES_B |
| ZX_REPORT_CODES_ASSOC | TABLE | 19 | This table stores reporting codes association info |
| ZX_REPORT_TYPES_USAGES | TABLE | 13 | This table stores Reporting Types info |
| ZX_REP_ACTG_EXT_T | TABLE | 58 | Interface table which is an extension of ZX_REP_TRX_DETAIL_T storing accounting information tied to ... |
| ZX_REP_AUDIT_DISTS | TABLE | 44 | This table contains the audit references for transaction tax reporting, including the references for... |
| ZX_REP_CONTEXT_T | TABLE | 42 | Used for Business Unit address information, if the report is run at the Ledger or Business Unit leve... |
| ZX_REP_TRX_DETAIL_T | TABLE | 459 | ZX_REP_TRX_DETAIL_T contains tax information for tax reporting purposes from Accounts Payable and Ac... |
| ZX_REP_TRX_JX_EXT_T | TABLE | 106 | Index for DETAIL_TAX_LINE_ID for table ZX_REP_TRX_JX_EXT_T |
| ZX_RULES_B | TABLE | 36 | This table stores the tax rules that are used to determine the outcome of multiple tax determination... |
| ZX_RULES_TL | TABLE | 11 | This table provides multilingual support (MLS) for each tax rule. MLS enables you to store and print... |
| ZX_SERVICE_TYPES | TABLE | 13 | This table stores tax service types, which are classifications used to categorize a tax service. For... |
| ZX_SIM_PURGE | TABLE | 10 | This table stores information which will be used for purging data created by the tax simulator. |
| ZX_SIM_TRX_DISTS | TABLE | 151 | This table stores Transaction Distribution info |
| ZX_SRVC_SBSCRPTN_EXCLS | TABLE | 11 | This table stores the list of event classes and applications that do not call the services of the ta... |
| ZX_SRVC_SUBSCRIPTIONS | TABLE | 14 | This table stores the list of service subscriptions for each regime of a first party organization de... |
| ZX_SRVC_TYP_PARAMS | TABLE | 15 | This table stores parameters for the service types. |
| ZX_STATUS_B | TABLE | 26 | This table stores tax statuses and the related attributes for multiple configuration owners. Each ro... |
| ZX_STATUS_TL | TABLE | 9 | This table provides multilingual support (MLS) for each tax status. MLS enables you to store and pri... |
| ZX_SUBSCRIPTION_DETAILS | TABLE | 15 | This table stores the details for each enabled content subscription option defined in ZX_SUBSCRIPTIO... |
| ZX_SUBSCRIPTION_OPTIONS | TABLE | 16 | This table stores the list of date effective content subscription options for each regime of a first... |
| ZX_TAXES_B | TABLE | 121 | This table stores taxes and the related attributes for multiple configuration owners. Each row store... |
| ZX_TAXES_TL | TABLE | 9 | This table provides multilingual support (MLS) for each tax. MLS enables you to store and print data... |
| ZX_TAX_SETTLEMENT_AUTHS_F | TABLE | 15 | This table contains information about tax authority assignment. |
| ZX_THREHLDS_SCHDL_CNTRLS_F | TABLE | 30 | This table contains detail information about thresholds for tax and jurisdictions. |
| ZX_TRANSACTION | TABLE | 119 | This tables stores Transaction info |
| ZX_TRANSACTION_LINES | TABLE | 257 | This table stores Transaction Lines info |
| ZX_TRX_LINE_APP_REGIMES | TABLE | 18 | This table stores Transaction Line aplicable Regimes |
| ZX_TRX_TAX_DISTRIBUTIONS | TABLE | 91 | This table contains the tax distributions information for the external or simulator tax transaction. |
| ZX_TRX_TELEMETRY_DATA | TABLE | 16 | This table stores the metrics for transactional tax API calls for a document for which the tax calcu... |
| ZX_WHT_EXEMPTION_DTLS | TABLE | 20 | This table stores withholding tax exemptions for supplier sites. Each record contains an exemption p... |
| ZX_WHT_LINES_SUMMARY | TABLE | 79 | This table stores withholding summary tax lines for transactions of multiple event classes. |
| ZX_WITHHOLDING_LINES | TABLE | 228 | This table contains information about withholding tax detail lines for transactions of multiple even... |

## Key joins between core objects

Child column -> parent key between the grouped objects above, taken from each page's Foreign Keys table. `joins.json` has every edge.

- `AR_ADJUSTMENTS_ALL.ASSOCIATED_APPLICATION_ID` -> `AR_RECEIVABLE_APPLICATIONS_ALL.RECEIVABLE_APPLICATION_ID`
- `AR_ADJUSTMENTS_ALL.ASSOCIATED_CASH_RECEIPT_ID` -> `AR_CASH_RECEIPTS_ALL.CASH_RECEIPT_ID`
- `AR_ADJUSTMENTS_ALL.BATCH_ID` -> `AR_BATCHES_ALL.BATCH_ID`
- `AR_ADJUSTMENTS_ALL.CHARGEBACK_CUSTOMER_TRX_ID` -> `RA_CUSTOMER_TRX_ALL.CUSTOMER_TRX_ID`
- `AR_ADJUSTMENTS_ALL.CONS_INV_ID` -> `AR_CONS_INV_ALL.CONS_INV_ID`
- `AR_ADJUSTMENTS_ALL.CUSTOMER_TRX_ID` -> `RA_CUSTOMER_TRX_ALL.CUSTOMER_TRX_ID`
- `AR_ADJUSTMENTS_ALL.CUSTOMER_TRX_LINE_ID` -> `RA_CUSTOMER_TRX_LINES_ALL.CUSTOMER_TRX_LINE_ID`
- `AR_ADJUSTMENTS_ALL.PAYMENT_SCHEDULE_ID` -> `AR_PAYMENT_SCHEDULES_ALL.PAYMENT_SCHEDULE_ID`
- `AR_ADJUSTMENTS_ALL.RECEIVABLES_TRX_ID, ORG_ID` -> `AR_RECEIVABLES_TRX_ALL.RECEIVABLES_TRX_ID/ORG_ID`
- `AR_ADJUSTMENTS_ALL.SUBSEQUENT_TRX_ID` -> `RA_CUSTOMER_TRX_ALL.CUSTOMER_TRX_ID`
- `AR_AGING_BUCKET_LINES_B.AGING_BUCKET_ID` -> `AR_AGING_BUCKETS.AGING_BUCKET_ID`
- `AR_BATCHES_ALL.BATCH_SOURCE_SEQ_ID` -> `AR_BATCH_SOURCES_ALL.BATCH_SOURCE_SEQ_ID`
- `AR_BATCHES_ALL.RECEIPT_CLASS_ID` -> `AR_RECEIPT_CLASSES.RECEIPT_CLASS_ID`
- `AR_BATCHES_ALL.RECEIPT_METHOD_ID` -> `AR_RECEIPT_METHODS.RECEIPT_METHOD_ID`
- `AR_CASH_RECEIPTS_ALL.CUSTOMER_SITE_USE_ID` -> `HZ_CUST_SITE_USES_ALL.SITE_USE_ID`
- `AR_CASH_RECEIPTS_ALL.PAY_FROM_CUSTOMER` -> `HZ_CUST_ACCOUNTS.CUST_ACCOUNT_ID`
- `AR_CASH_RECEIPTS_ALL.RECEIPT_METHOD_ID` -> `AR_RECEIPT_METHODS.RECEIPT_METHOD_ID`
- `AR_CASH_RECEIPTS_ALL.RECEIVABLES_TRX_ID, ORG_ID` -> `AR_RECEIVABLES_TRX_ALL.RECEIVABLES_TRX_ID/ORG_ID`
- `AR_CASH_RECEIPTS_ALL.SELECTED_REMITTANCE_BATCH_ID` -> `AR_BATCHES_ALL.BATCH_ID`
- `AR_CASH_RECEIPT_HISTORY_ALL.BATCH_ID` -> `AR_BATCHES_ALL.BATCH_ID`
- `AR_CASH_RECEIPT_HISTORY_ALL.CASH_RECEIPT_ID` -> `AR_CASH_RECEIPTS_ALL.CASH_RECEIPT_ID`
- `AR_CONS_INV_ALL.CUSTOMER_ID` -> `HZ_CUST_ACCOUNTS.CUST_ACCOUNT_ID`
- `AR_CONS_INV_ALL.SITE_USE_ID` -> `HZ_CUST_SITE_USES_ALL.SITE_USE_ID`
- `AR_CONS_INV_ALL.TERM_ID` -> `RA_TERMS_B.TERM_ID`
- `AR_DEFERRED_LINES_ALL.CUSTOMER_TRX_ID` -> `RA_CUSTOMER_TRX_ALL.CUSTOMER_TRX_ID`
- `AR_DEFERRED_LINES_ALL.CUSTOMER_TRX_LINE_ID` -> `RA_CUSTOMER_TRX_LINES_ALL.CUSTOMER_TRX_LINE_ID`
- `AR_DISPUTE_HISTORY.PAYMENT_SCHEDULE_ID` -> `AR_PAYMENT_SCHEDULES_ALL.PAYMENT_SCHEDULE_ID`
- `AR_DISTRIBUTIONS_ALL.THIRD_PARTY_ID` -> `HZ_CUST_ACCOUNTS.CUST_ACCOUNT_ID`
- `AR_PAYMENT_SCHEDULES_ALL.ADJUSTMENT_ID_LAST` -> `AR_ADJUSTMENTS_ALL.ADJUSTMENT_ID`
- `AR_PAYMENT_SCHEDULES_ALL.ASSOCIATED_CASH_RECEIPT_ID` -> `AR_CASH_RECEIPTS_ALL.CASH_RECEIPT_ID`
- `AR_PAYMENT_SCHEDULES_ALL.CASH_APPLIED_ID_LAST` -> `AR_RECEIVABLE_APPLICATIONS_ALL.RECEIVABLE_APPLICATION_ID`
- `AR_PAYMENT_SCHEDULES_ALL.CASH_RECEIPT_ID` -> `AR_CASH_RECEIPTS_ALL.CASH_RECEIPT_ID`
- `AR_PAYMENT_SCHEDULES_ALL.CASH_RECEIPT_ID_LAST` -> `AR_CASH_RECEIPTS_ALL.CASH_RECEIPT_ID`
- `AR_PAYMENT_SCHEDULES_ALL.COLLECTOR_LAST` -> `AR_COLLECTORS.COLLECTOR_ID`
- `AR_PAYMENT_SCHEDULES_ALL.CONS_INV_ID` -> `AR_CONS_INV_ALL.CONS_INV_ID`
- `AR_PAYMENT_SCHEDULES_ALL.CONS_INV_ID_REV` -> `AR_CONS_INV_ALL.CONS_INV_ID`
- `AR_PAYMENT_SCHEDULES_ALL.CUSTOMER_ID` -> `HZ_CUST_ACCOUNTS.CUST_ACCOUNT_ID`
- `AR_PAYMENT_SCHEDULES_ALL.CUSTOMER_SITE_USE_ID` -> `HZ_CUST_SITE_USES_ALL.SITE_USE_ID`
- `AR_PAYMENT_SCHEDULES_ALL.CUSTOMER_TRX_ID` -> `RA_CUSTOMER_TRX_ALL.CUSTOMER_TRX_ID`
- `AR_PAYMENT_SCHEDULES_ALL.CUST_TRX_TYPE_SEQ_ID` -> `RA_CUST_TRX_TYPES_ALL.CUST_TRX_TYPE_SEQ_ID`
- `AR_PAYMENT_SCHEDULES_ALL.REVERSED_CASH_RECEIPT_ID` -> `AR_CASH_RECEIPTS_ALL.CASH_RECEIPT_ID`
- `AR_PAYMENT_SCHEDULES_ALL.SELECTED_FOR_RECEIPT_BATCH_ID` -> `AR_BATCHES_ALL.BATCH_ID`
- `AR_PAYMENT_SCHEDULES_ALL.TERM_ID` -> `RA_TERMS_B.TERM_ID`
- `AR_RECEIPT_METHODS.RECEIPT_CLASS_ID` -> `AR_RECEIPT_CLASSES.RECEIPT_CLASS_ID`
- `AR_RECEIPT_METHOD_ACCOUNTS_ALL.EDISC_RECEIVABLES_TRX_ID, ORG_ID` -> `AR_RECEIVABLES_TRX_ALL.RECEIVABLES_TRX_ID/ORG_ID`
- `AR_RECEIPT_METHOD_ACCOUNTS_ALL.RECEIPT_METHOD_ID` -> `AR_RECEIPT_METHODS.RECEIPT_METHOD_ID`
- `AR_RECEIPT_METHOD_ACCOUNTS_ALL.UNEDISC_RECEIVABLES_TRX_ID, ORG_ID` -> `AR_RECEIVABLES_TRX_ALL.RECEIVABLES_TRX_ID/ORG_ID`
- `AR_RECEIVABLE_APPLICATIONS_ALL.APPLIED_CUSTOMER_TRX_ID` -> `RA_CUSTOMER_TRX_ALL.CUSTOMER_TRX_ID`
- `AR_RECEIVABLE_APPLICATIONS_ALL.APPLIED_CUSTOMER_TRX_LINE_ID` -> `RA_CUSTOMER_TRX_LINES_ALL.CUSTOMER_TRX_LINE_ID`
- `AR_RECEIVABLE_APPLICATIONS_ALL.APPLIED_PAYMENT_SCHEDULE_ID` -> `AR_PAYMENT_SCHEDULES_ALL.PAYMENT_SCHEDULE_ID`
- `AR_RECEIVABLE_APPLICATIONS_ALL.CASH_RECEIPT_HISTORY_ID` -> `AR_CASH_RECEIPT_HISTORY_ALL.CASH_RECEIPT_HISTORY_ID`
- `AR_RECEIVABLE_APPLICATIONS_ALL.CASH_RECEIPT_ID` -> `AR_CASH_RECEIPTS_ALL.CASH_RECEIPT_ID`
- `AR_RECEIVABLE_APPLICATIONS_ALL.CUSTOMER_TRX_ID` -> `RA_CUSTOMER_TRX_ALL.CUSTOMER_TRX_ID`
- `AR_RECEIVABLE_APPLICATIONS_ALL.PAYMENT_SCHEDULE_ID` -> `AR_PAYMENT_SCHEDULES_ALL.PAYMENT_SCHEDULE_ID`
- `AR_RECEIVABLE_APPLICATIONS_ALL.RECEIVABLES_TRX_ID, ORG_ID` -> `AR_RECEIVABLES_TRX_ALL.RECEIVABLES_TRX_ID/ORG_ID`
- `AR_SYSTEM_PARAMETERS_ALL.EXCEPTION_ADJ_REC_TRX_ID, ORG_ID` -> `AR_RECEIVABLES_TRX_ALL.RECEIVABLES_TRX_ID/ORG_ID`
- `AR_SYSTEM_PARAMETERS_ALL.EXCEPTION_WRTOFF_REC_TRX_ID, ORG_ID` -> `AR_RECEIVABLES_TRX_ALL.RECEIVABLES_TRX_ID/ORG_ID`
- `AR_SYSTEM_PARAMETERS_ALL.FINCHRG_RECEIVABLES_TRX_ID, ORG_ID` -> `AR_RECEIVABLES_TRX_ALL.RECEIVABLES_TRX_ID/ORG_ID`
- `AR_SYSTEM_PARAMETERS_ALL.IREC_SERVICE_CHARGE_REC_TRX_ID, ORG_ID` -> `AR_RECEIVABLES_TRX_ALL.RECEIVABLES_TRX_ID/ORG_ID`
- `AR_SYSTEM_PARAMETERS_ALL.LATE_CHARGE_BAT_SOURCE_SEQ_ID` -> `RA_BATCH_SOURCES_ALL.BATCH_SOURCE_SEQ_ID`
- `AR_SYSTEM_PARAMETERS_ALL.LATE_CHARGE_DM_TYPE_SEQ_ID` -> `RA_CUST_TRX_TYPES_ALL.CUST_TRX_TYPE_SEQ_ID`
- `AR_SYSTEM_PARAMETERS_ALL.LATE_CHARGE_INV_TYPE_SEQ_ID` -> `RA_CUST_TRX_TYPES_ALL.CUST_TRX_TYPE_SEQ_ID`
- `AR_SYSTEM_PARAMETERS_ALL.PENALTY_REC_TRX_ID, ORG_ID` -> `AR_RECEIVABLES_TRX_ALL.RECEIVABLES_TRX_ID/ORG_ID`
- `HZ_CUST_ACCOUNTS.PARTY_ID` -> `HZ_PARTIES.PARTY_ID`
- `HZ_CUST_ACCOUNTS.SELLING_PARTY_ID` -> `HZ_PARTIES.PARTY_ID`
- `HZ_CUST_ACCT_SITES_ALL.CUST_ACCOUNT_ID` -> `HZ_CUST_ACCOUNTS.CUST_ACCOUNT_ID`
- `HZ_CUST_ACCT_SITES_ALL.PARTY_SITE_ID` -> `HZ_PARTY_SITES.PARTY_SITE_ID`
- `HZ_CUST_SITE_USES_ALL.CUST_ACCT_SITE_ID` -> `HZ_CUST_ACCT_SITES_ALL.CUST_ACCT_SITE_ID`
- `HZ_PARTY_SITES.LOCATION_ID` -> `HZ_LOCATIONS.LOCATION_ID`
- `HZ_PARTY_SITES.PARTY_ID` -> `HZ_PARTIES.PARTY_ID`
- `RA_BATCH_SOURCES_ALL.DEFAULT_INV_TRX_TYPE_SEQ_ID` -> `RA_CUST_TRX_TYPES_ALL.CUST_TRX_TYPE_SEQ_ID`
- `RA_CUSTOMER_TRX_ALL.BATCH_SOURCE_SEQ_ID` -> `RA_BATCH_SOURCES_ALL.BATCH_SOURCE_SEQ_ID`
- `RA_CUSTOMER_TRX_ALL.BILL_TO_ADDRESS_ID` -> `HZ_CUST_ACCT_SITES_ALL.CUST_ACCT_SITE_ID`
- `RA_CUSTOMER_TRX_ALL.BILL_TO_CUSTOMER_ID` -> `HZ_CUST_ACCOUNTS.CUST_ACCOUNT_ID`
- `RA_CUSTOMER_TRX_ALL.BILL_TO_SITE_USE_ID` -> `HZ_CUST_SITE_USES_ALL.SITE_USE_ID`
- `RA_CUSTOMER_TRX_ALL.CUST_TRX_TYPE_SEQ_ID` -> `RA_CUST_TRX_TYPES_ALL.CUST_TRX_TYPE_SEQ_ID`
- `RA_CUSTOMER_TRX_ALL.PAYING_CUSTOMER_ID` -> `HZ_CUST_ACCOUNTS.CUST_ACCOUNT_ID`
- `RA_CUSTOMER_TRX_ALL.PAYING_SITE_USE_ID` -> `HZ_CUST_SITE_USES_ALL.SITE_USE_ID`
- `RA_CUSTOMER_TRX_ALL.RECEIPT_METHOD_ID` -> `AR_RECEIPT_METHODS.RECEIPT_METHOD_ID`
- `RA_CUSTOMER_TRX_ALL.RELATED_BATCH_SOURCE_SEQ_ID` -> `RA_BATCH_SOURCES_ALL.BATCH_SOURCE_SEQ_ID`
- `RA_CUSTOMER_TRX_ALL.REMITTANCE_BATCH_ID` -> `AR_BATCHES_ALL.BATCH_ID`
- `RA_CUSTOMER_TRX_ALL.REMIT_TO_ADDRESS_ID` -> `HZ_CUST_ACCT_SITES_ALL.CUST_ACCT_SITE_ID`
- `RA_CUSTOMER_TRX_ALL.REVERSED_CASH_RECEIPT_ID` -> `AR_CASH_RECEIPTS_ALL.CASH_RECEIPT_ID`
- `RA_CUSTOMER_TRX_ALL.SHIP_TO_ADDRESS_ID` -> `HZ_CUST_ACCT_SITES_ALL.CUST_ACCT_SITE_ID`
- `RA_CUSTOMER_TRX_ALL.SHIP_TO_CUSTOMER_ID` -> `HZ_CUST_ACCOUNTS.CUST_ACCOUNT_ID`
- `RA_CUSTOMER_TRX_ALL.SHIP_TO_PARTY_ADDRESS_ID` -> `HZ_PARTY_SITES.PARTY_SITE_ID`
- `RA_CUSTOMER_TRX_ALL.SHIP_TO_PARTY_ID` -> `HZ_PARTIES.PARTY_ID`
- `RA_CUSTOMER_TRX_ALL.SHIP_TO_SITE_USE_ID` -> `HZ_CUST_SITE_USES_ALL.SITE_USE_ID`
- `RA_CUSTOMER_TRX_ALL.SOLD_TO_CUSTOMER_ID` -> `HZ_CUST_ACCOUNTS.CUST_ACCOUNT_ID`
- `RA_CUSTOMER_TRX_ALL.SOLD_TO_PARTY_ID` -> `HZ_PARTIES.PARTY_ID`
- `RA_CUSTOMER_TRX_ALL.SOLD_TO_SITE_USE_ID` -> `HZ_CUST_SITE_USES_ALL.SITE_USE_ID`
- `RA_CUSTOMER_TRX_ALL.TERM_ID` -> `RA_TERMS_B.TERM_ID`
- `RA_CUSTOMER_TRX_LINES_ALL.CUSTOMER_TRX_ID` -> `RA_CUSTOMER_TRX_ALL.CUSTOMER_TRX_ID`
- `RA_CUSTOMER_TRX_LINES_ALL.PREPAY_CUSTOMER_TRX_ID` -> `RA_CUSTOMER_TRX_ALL.CUSTOMER_TRX_ID`
- `RA_CUSTOMER_TRX_LINES_ALL.PREVIOUS_CUSTOMER_TRX_ID` -> `RA_CUSTOMER_TRX_ALL.CUSTOMER_TRX_ID`
- `RA_CUSTOMER_TRX_LINES_ALL.SHIP_TO_ADDRESS_ID` -> `HZ_CUST_ACCT_SITES_ALL.CUST_ACCT_SITE_ID`
- `RA_CUSTOMER_TRX_LINES_ALL.SHIP_TO_CUSTOMER_ID` -> `HZ_CUST_ACCOUNTS.CUST_ACCOUNT_ID`
- `RA_CUSTOMER_TRX_LINES_ALL.SHIP_TO_PARTY_ADDRESS_ID` -> `HZ_PARTY_SITES.PARTY_SITE_ID`
- `RA_CUSTOMER_TRX_LINES_ALL.SHIP_TO_PARTY_ID` -> `HZ_PARTIES.PARTY_ID`
- `RA_CUST_TRX_LINE_GL_DIST_ALL.CUSTOMER_TRX_ID` -> `RA_CUSTOMER_TRX_ALL.CUSTOMER_TRX_ID`
- `RA_CUST_TRX_LINE_GL_DIST_ALL.CUSTOMER_TRX_LINE_ID` -> `RA_CUSTOMER_TRX_LINES_ALL.CUSTOMER_TRX_LINE_ID`
- `RA_CUST_TRX_LINE_GL_DIST_ALL.CUST_TRX_LINE_SALESREP_ID` -> `RA_CUST_TRX_LINE_SALESREPS_ALL.CUST_TRX_LINE_SALESREP_ID`
- `RA_CUST_TRX_LINE_SALESREPS_ALL.CUSTOMER_TRX_ID` -> `RA_CUSTOMER_TRX_ALL.CUSTOMER_TRX_ID`
- `RA_INTERFACE_LINES_ALL.CUSTOMER_TRX_ID` -> `RA_CUSTOMER_TRX_ALL.CUSTOMER_TRX_ID`
- `RA_INTERFACE_LINES_ALL.CUST_TRX_TYPE_SEQ_ID` -> `RA_CUST_TRX_TYPES_ALL.CUST_TRX_TYPE_SEQ_ID`
- `RA_INTERFACE_LINES_ALL.INITIAL_CUSTOMER_TRX_ID` -> `RA_CUSTOMER_TRX_ALL.CUSTOMER_TRX_ID`
- `RA_INTERFACE_LINES_ALL.INTERFACE_LINE_ID` -> `RA_CUSTOMER_TRX_ALL.CUSTOMER_TRX_ID`
- `RA_INTERFACE_LINES_ALL.ORIG_SYSTEM_BILL_ADDRESS_ID` -> `HZ_CUST_ACCT_SITES_ALL.CUST_ACCT_SITE_ID`
- `RA_INTERFACE_LINES_ALL.ORIG_SYSTEM_BILL_CUSTOMER_ID` -> `HZ_CUST_ACCOUNTS.CUST_ACCOUNT_ID`
- `RA_INTERFACE_LINES_ALL.ORIG_SYSTEM_SHIP_ADDRESS_ID` -> `HZ_CUST_ACCT_SITES_ALL.CUST_ACCT_SITE_ID`
- `RA_INTERFACE_LINES_ALL.ORIG_SYSTEM_SHIP_CUSTOMER_ID` -> `HZ_CUST_ACCOUNTS.CUST_ACCOUNT_ID`
- `RA_INTERFACE_LINES_ALL.ORIG_SYSTEM_SOLD_CUSTOMER_ID` -> `HZ_CUST_ACCOUNTS.CUST_ACCOUNT_ID`
- `RA_INTERFACE_LINES_ALL.ORIG_SYS_SHIP_PARTY_ID` -> `HZ_PARTIES.PARTY_ID`
- `RA_INTERFACE_LINES_ALL.ORIG_SYS_SHIP_PARTY_SITE_ID` -> `HZ_PARTY_SITES.PARTY_SITE_ID`
- `RA_INTERFACE_LINES_ALL.ORIG_SYS_SOLD_PARTY_ID` -> `HZ_PARTIES.PARTY_ID`
- `RA_INTERFACE_LINES_ALL.PAYING_CUSTOMER_ID` -> `HZ_CUST_ACCOUNTS.CUST_ACCOUNT_ID`
- `RA_INTERFACE_LINES_ALL.PAYING_SITE_USE_ID` -> `HZ_CUST_SITE_USES_ALL.SITE_USE_ID`
- `RA_INTERFACE_LINES_ALL.PREPAY_CUSTOMER_TRX_ID` -> `RA_CUSTOMER_TRX_ALL.CUSTOMER_TRX_ID`
- `RA_INTERFACE_LINES_ALL.PREPAY_CUSTOMER_TRX_LINE_ID` -> `RA_CUSTOMER_TRX_LINES_ALL.CUSTOMER_TRX_LINE_ID`
- `RA_INTERFACE_LINES_ALL.PREVIOUS_CUSTOMER_TRX_ID` -> `RA_CUSTOMER_TRX_ALL.CUSTOMER_TRX_ID`
- `RA_INTERFACE_LINES_ALL.RECEIPT_METHOD_ID` -> `AR_RECEIPT_METHODS.RECEIPT_METHOD_ID`
- `RA_INTERFACE_LINES_ALL.REFERENCE_LINE_ID` -> `RA_CUSTOMER_TRX_LINES_ALL.CUSTOMER_TRX_LINE_ID`
- `RA_INTERFACE_LINES_ALL.RELATED_CUSTOMER_TRX_ID` -> `RA_CUSTOMER_TRX_ALL.CUSTOMER_TRX_ID`
- `RA_INTERFACE_LINES_ALL.SOURCE_TRX_LINE_ID` -> `RA_CUSTOMER_TRX_LINES_ALL.CUSTOMER_TRX_LINE_ID`
- `RA_INTERFACE_LINES_ALL.TERM_ID` -> `RA_TERMS_B.TERM_ID`
- `RA_TERMS_LINES.TERM_ID` -> `RA_TERMS_B.TERM_ID`
