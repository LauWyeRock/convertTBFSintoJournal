# Columns : 
# Journal Reference, Contact, Date, Account, Description, Tax Included in Amount, Debit Amount, Credit Amount


# (i) QB has missing accounts in TB that are needed for P&L/BS 

# (ii) Review all 3 files: TB, BS, P&L, and find all the unique/distinct accounts.
# (iii) Print each of those unique accounts as row values in our journal import template (example attached) under "Account" column

# (iv) For accounts that do not show up on TB -- just leave blank for debit and credit

# (v) "Reference" for each row "FYE2023 Conversion: Transfer Balance"

# (vi) Add 4 extra columns in the output file that indicate the original values for each account
# ### "TB Debit" // "TB Credit" // "BS Amount" // "P&L Amount"
# ### For each account, show the value from the original file
# ### Some accounts show up on 2 files, so you print 2 amounts