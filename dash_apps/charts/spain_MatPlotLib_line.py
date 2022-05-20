'''Contributers:Tasha Tahir, Yuansheng Zhang'''

from dash_apps.sqlite import SQLite
from matplotlib import pyplot as plt


def spain_MatPlotLib_line():
    database = SQLite('data/Updated_EuroStat.db')

    country_list_0 = ['Italy', 'Spain']
    country_list_1 = ['Malta', 'Portugal', 'Serbia', 'Slovenia', 'Greece']

    years = range(2010, 2017+1)
    def get_data (country_list):
        data = database.get_data_for_countries(countries=country_list)
        data_by_country = {}
        for row in data:
            data_by_country.setdefault(row.get('country'), []).append(row.get('investments') or 0)
        return data_by_country, years

    fig, axs = plt.subplots(2)
    bars = []
    # add the upper graph
    for country, investments in get_data(country_list_0)[0].items():
        bars.append(axs[0].plot(
            years,
            investments,
            label=country
        ))

    # add the lower graph
    for country, investments in get_data(country_list_1)[0].items():
        bars.append(axs[1].plot(
            years,
            investments,
            label=country
        ))

    # Add features
    fig.suptitle('Raw Investments Of All South EU Countries Each Year')
    axs[0].set_ylabel('Investment (Million EUR)')
    axs[1].set_ylabel('Investment (Million EUR)')
    axs[1].set_xlabel('Year')
    axs[0].grid()
    axs[1].grid()
    axs[0].legend(bbox_to_anchor=(1.0, 1.0), loc='upper left')
    axs[1].legend(bbox_to_anchor=(1.0, 1.0), loc='upper left')
    fig.tight_layout()

    url = 'my_app/static/img/spain_MatPlotLib_line.png'
    fig.savefig( url )

    return url
