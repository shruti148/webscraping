import pandas as pd
import numpy as np
from flask import render_template, url_for, flash, redirect, request, make_response, jsonify, abort
from web import app
import json
import matplotlib
matplotlib.use('Agg')
from flask import Flask, render_template, request
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.dates import DateFormatter
from matplotlib import pyplot
import warnings; warnings.simplefilter('ignore')
from io import BytesIO
import base64
import plotly
import plotly.graph_objects as go
import plotly.express as px
import os

covid19_df = pd.read_csv("web/static/covid_19_india(1).csv")
Testing = pd.read_csv("web/static/StatewiseTestingDetails.csv")
Testing.Negative = Testing.Negative.fillna('0')
Testing.Positive = Testing.Positive.fillna('0')
Testing = Testing.astype({'Positive': 'int32'})

covid19_df.rename(columns={'State/UnionTerritory':'State'},inplace=True)
covid19_df=covid19_df.replace('Telengana','Telangana')
covid19_df=covid19_df.replace('Telengana***','Telangana')
covid19_df=covid19_df.replace('Telangana***','Telangana')
covid19_df=covid19_df.replace('Maharashtra***','Maharashtra')
covid19_df=covid19_df.replace('Chandigarh***','Chandigarh')
covid19_df=covid19_df.replace('Punjab***','Punjab')
dropn_indexnames =covid19_df[(covid19_df['State'] == 'Cases being reassigned to states')].index
covid19_df.drop(dropn_indexnames,inplace=True)

df = covid19_df.tail(35) ## Extract most recent date's info & data
df1 = df.sort_values(by='Confirmed', ascending=False).head(10)

dat=pd.read_csv("web/static/database.csv")

@app.route("/state", methods=['POST'])
def plot_state():
    # total confirmed cases globally
    # take country input from user
    State_name = request.form['state_name']
    print(State_name)
    inf = covid19_df[covid19_df.State == State_name]

    req = inf[inf['Date'].isin(['09/03/20','09/04/20','09/05/20','09/06/20','09/07/20','09/08/20','09/09/20','09/10/20','09/11/20','09/12/20'])]
# ----------------------Using Matplotlib---------------------------------------------------
    # a4_dims = (7,5)
    # # datx=("m1","m10","m11","m12","m13","m14","m15","m16","m17","m18",)
    # fig, ax = pyplot.subplots(figsize=a4_dims)
    # pp = sns.lineplot(data=req,x='Date',y='Confirmed',ax=ax,color='Blue')
    # pp = sns.lineplot(data=req,x='Date',y='Cured',ax=ax,color='Green')
    # pp = sns.lineplot(data=req,x='Date',y='Deaths',ax=ax,color='Red')
    # pp.set_yticklabels(labels=(pp.get_yticks()*1).astype(int))
    # fig.legend(labels=['Confirmed','Cured','Deaths'])
    # plt.title('Vulnerability summary of State',size=15)
    # img11 = BytesIO()
    # plt.savefig(img11, format='png')
    # plt.close()
    # img11.seek(0)
    # plot_vul = base64.b64encode(img11.getvalue()).decode('utf8')
# ----------------Using plotly-------------------------------------------------------------------



    fig8 = px.line(req, x="Date", y=["Confirmed",'Cured','Deaths'],title='Vulnerability summary of State' )
    plot_vul = json.dumps(fig8, cls=plotly.utils.PlotlyJSONEncoder)


# ---------------------------------------------------------------------------------
    test_maha = Testing[Testing.State == State_name]
    reqe = test_maha[test_maha['Date'].isin(['2020-04-05','2020-05-05','2020-06-05','2020-07-05','2020-08-05','2020-09-05','2020-10-05','2020-11-05','2020-12-05'])]
    #
    # a4_dims = (7,5)
    # fig, ax = pyplot.subplots(figsize=a4_dims)
    # lp = sns.lineplot(x='Date',y='TotalSamples',data=reqe,ax=ax,color='brown')
    # lp.set_yticklabels(labels=(lp.get_yticks()*1).astype(int))
    # plt.title('Testing in state',size=15)
    # img12 = BytesIO()
    # plt.savefig(img12, format='png')
    # plt.close()
    # img12.seek(0)
    # plot_testing = base64.b64encode(img12.getvalue()).decode('utf8')
    # ------------------------------------------------------------------

    fig9 = px.line(reqe, x='Date', y="TotalSamples", title='Testing in state')
    plot_testing = json.dumps(fig9, cls=plotly.utils.PlotlyJSONEncoder)



# -----------------------------------------------------------------------------------------
    test_maha = Testing[Testing.State == State_name]
    reqe = test_maha[test_maha['Date'].isin(['2020-04-05','2020-05-05','2020-06-05','2020-07-05','2020-08-05','2020-09-05','2020-10-05','2020-11-05','2020-12-05'])]

    # a4_dims = (7,5)
    # fig, ax = pyplot.subplots(figsize=a4_dims)
    # reqe['positive/samples'] = (reqe['Positive']/reqe['TotalSamples'])
    # df =reqe.iloc[1:7]
    # sns.lineplot(x='Date',y='positive/samples',ax=ax,data=df)
    # plt.title('Positive Cases per Samples in state',size=15)
    # img13 = BytesIO()
    # plt.savefig(img13, format='png')
    # plt.close()
    # img13.seek(0)
    # plot_poscase = base64.b64encode(img13.getvalue()).decode('utf8')
    # -------------------------------------------------------------------------------
    reqe['positive/samples'] = (reqe['Positive']/reqe['TotalSamples'])
    df =reqe.iloc[1:7]
    fig9 = px.line(df, x='Date', y="positive/samples", title='Positive Cases per Samples in Maharashtra')
    plot_poscase = json.dumps(fig9, cls=plotly.utils.PlotlyJSONEncoder)



# --------------------------------------------------------------------------------------------------------
    Mah = dat[dat.States ==State_name]
    total_active_per_country=(Mah["Total Active case"])
    total_active_per_country=list(total_active_per_country)[0]

    total_recovered_per_country=(Mah["Total cured cases"])
    total_recovered_per_country=list(total_recovered_per_country)[0]

    total_death_per_country=(Mah["Total deaths"])
    total_death_per_country=list(total_death_per_country)[0]


    # --------------------------------------------------------------------------------------------------------
    context = {"plot_vul": plot_vul,"plot_testing": plot_testing, "plot_poscase": plot_poscase,
    "total_active_per_country": total_active_per_country,"total_recovered_per_country": total_recovered_per_country,
    "total_death_per_country": total_death_per_country,"State_name":State_name}
    return render_template('state.html', context=context)


# ---------------------------------------------------------------------------------------------------
@app.route("/")

def concase():
    print("here")
# --------Using Matplotlib------------------------------------------------------------------
    # covid19 = dat.sort_values(by=['Total Active case'],ascending = False)
    # plt.figure(figsize=(10,5),dpi = 80)
    # plt.bar(covid19['States'][:5],covid19['Total Active case'][:5],align='center')
    # plt.ylabel('Number of confirmed cases')
    # plt.title('States with maximum confirmed cases')
    # # div = plt.to_html(full_html=False)
    # img = BytesIO()
    # plt.savefig(img, format='png')
    # plt.close()
    # img.seek(0)
    # plot_url = base64.b64encode(img.getvalue()).decode('utf8')

# -------------------Using Plotly-----------------------------------------------------------------
    covid19 = dat.sort_values(by=['Total Active case'],ascending = False)
    fig = px.bar(covid19,
                 x=covid19['States'][:5],
                 y=covid19['Total Active case'][:5],
                 color=covid19['States'][:5],
                 barmode='stack',
                 title='States with maximum confirmed cases')
    plot_url = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

# ----------------------------------------------------------------------
    # covid19 = dat.sort_values(by=['Total Active case'],ascending = False)
    # plt.figure(figsize=(10,5),dpi = 80)
    # plt.bar(covid19['States'][:5],covid19['Total cured cases'][:5],align='center')
    # plt.ylabel('Number of cured cases')
    # plt.title('States with maximum cured cases')
    # img1 = BytesIO()
    # plt.savefig(img1, format='png')
    # plt.close()
    # img1.seek(0)
    # plot_cure = base64.b64encode(img1.getvalue()).decode('utf8')


    covid19 = dat.sort_values(by=['Total Active case'],ascending = False)
    fig1 = px.bar(covid19,
                 x=covid19['States'][:5],
                 y=covid19['Total cured cases'][:5],
                 color=covid19['States'][:5],
                 barmode='stack',
                 title='States with maximum cured cases')
    plot_cure = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)


# ---------------------------------------------------------------------------------
    # covid19 = dat.sort_values(by=['Total Active case'],ascending = False)
    # plt.figure(figsize=(10,5),dpi = 80)
    # plt.bar(covid19['States'][:5],covid19['Total deaths'][:5],align='center')
    # plt.ylabel('Number of Deaths')
    # plt.title('States with maximum death cases')
    # img = BytesIO()
    # plt.savefig(img, format='png')
    # plt.close()
    # img.seek(0)
    # plot_death = base64.b64encode(img.getvalue()).decode('utf8')

    covid19 = dat.sort_values(by=['Total Active case'],ascending = False)
    fig2 = px.bar(covid19,
                 x=covid19['States'][:5],
                 y=covid19['Total deaths'][:5],
                 color=covid19['States'][:5],
                 barmode='stack',
                 title='States with maximum death cases')
    plot_death = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)



# --------------------------------------------------------------------------------------
    context = {"plot_url": plot_url,"plot_cure": plot_cure,"plot_death":plot_death}

    return render_template('plotly.html', context=context)

@app.route("/plotly")
def chart():
    covid19 = dat.sort_values(by=['Total Active case'],ascending = False)

    sed=covid19['States'][:5]
    fig7 = go.Figure(data = [
        go.Bar(name = 'Recovered Cases', x = sed, y = covid19['Total cured cases'][:5]),
        go.Bar(name = 'Active Cases', x = sed, y = covid19['Total Active case'][:5]),
        go.Bar(name = 'Death Cases', x = sed, y = covid19['Total deaths'][:5])
    ])
    fig7.update_layout(title = 'Most Affected States in India', barmode = 'stack', height = 600)
    plot_death = json.dumps(fig7, cls=plotly.utils.PlotlyJSONEncoder)
    context={"plot_death":plot_death}
    return render_template('chart.html', context=context)
