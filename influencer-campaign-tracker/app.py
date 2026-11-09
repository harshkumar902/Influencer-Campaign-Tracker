import pandas as pd
import streamlit as st
from pathlib import Path
st.set_page_config(page_title="Creator Campaigns",layout="wide")
st.title("Influencer Campaign Tracker")
up=st.file_uploader("Upload creator tracking CSV",type="csv")
df=pd.read_csv(up if up else Path(__file__).with_name("sample_creators.csv"))
required={"creator","platform","status","fee","product_cost","attributed_orders","attributed_revenue"}
if not required.issubset(df.columns):st.error("CSV missing: "+", ".join(sorted(required-set(df.columns))));st.stop()
for c in ["fee","product_cost","attributed_orders","attributed_revenue"]:df[c]=pd.to_numeric(df[c],errors="coerce").fillna(0)
df["total_cost"]=df.fee+df.product_cost
df["reported_roas"]=df.apply(lambda r:round(r.attributed_revenue/r.total_cost,2) if r.total_cost>0 else None,axis=1)
statuses=st.multiselect("Statuses",sorted(df.status.unique()),default=sorted(df.status.unique()))
view=df[df.status.isin(statuses)].copy()
a,b,c=st.columns(3)
a.metric("Creator spend + samples",f"₹{view.total_cost.sum():,.0f}")
b.metric("Attributed revenue",f"₹{view.attributed_revenue.sum():,.0f}")
c.metric("Attributed orders",int(view.attributed_orders.sum()))
st.dataframe(view,use_container_width=True)
st.bar_chart(view.set_index("creator")[["total_cost","attributed_revenue"]])
st.download_button("Export campaign tracking",view.to_csv(index=False).encode(),"creator_campaigns.csv","text/csv")
st.caption("Attribution numbers are input data and may not represent incremental sales. Creators and amounts in sample are fictional.")
