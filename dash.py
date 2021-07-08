'''
This is where I will actually make my 
daily dashboard to monitor my stocks.
'''


#%%

import ingest

with open('../data/stocks.txt') as f:
    raw = f.read()
    
df = ingest.ingest(raw)

# %%
