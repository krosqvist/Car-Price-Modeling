import pandas as pd
import numpy as np

def market_trend_generalizator(df, start_year, end_year, top_n=20):
    #filter by the given years
    df_in_range = df[(df["Adv_year"] >= start_year) & (df["Adv_year"] <= end_year)].copy()

    # grab the most advertised cars
    top_models = df_in_range["Genmodel"].value_counts().head(top_n).index
    df_top = df_in_range[df_in_range["Genmodel"].isin(top_models)].copy()

    # correction for inflation
    df_top["Price_infl_adj"] = df_top["Price"] * df_top["Inflation_index"]
    df_top["Entry_price_infl_adj"] = df_top["Entry_price"] * df_top["Inflation_index_entry"]


    # turn into percentages to make the y values "similar"
    df_top["price_percentage"] = (df_top["Price_infl_adj"] / df_top["Entry_price_infl_adj"])

    # combine
    market_summary = (df_top.groupby("Adv_year")["price_percentage"].agg(["mean","std","count"]).reset_index())
    return market_summary
