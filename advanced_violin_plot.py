import plotly.graph_objects as go
import pandas as pd

# Load your dataframe here
#df = pd.read_excel("path_to_your_file.xlsx")
df = pd.read_csv("tables/numbers of specimens normalized_for statistcl analysis.xlsx - Normalized_abundances.csv")


# Определение цветов для каждой комбинации Habitat и Site
colors = {
    'L_SB': 'lightgreen',
    'L_NB': 'green',
    'SIM_SB': 'yellow',
    'SIM_NB': 'orange',
    'SOM_SB': 'maroon',
    'SOM_NB': 'red'
}
pointpos_SB = [-0.9,-1.1,-0.6,-0.3]
pointpos_NB = [0.45,0.55,1,0.4]
show_legend = [True,False,False,False]
# Получаем уникальные среды обитания и виды
unique_habitats = df['Habitat'].unique()
species_columns = df.columns[3:11]  # Измените индексы в соответствии с вашими данными

# Создаем по отдельному графику для каждого вида
for species in species_columns:
    fig = go.Figure()

    for habitat in unique_habitats:

        # Фильтруем данные для каждой среды обитания и каждого сайта
        habitat_data = df[df['Habitat'] == habitat]
        habitat_sb_data = habitat_data[habitat_data['Site'] == 'SB'][species]
        habitat_nb_data = habitat_data[habitat_data['Site'] == 'NB'][species]

        # Устанавливаем значение pointpos так, чтобы точки находились ближе к краям виолончели
        pointpos = 1.4

        # Добавляем виолончель для SB
        fig.add_trace(go.Violin(y=habitat_sb_data,
                                x=[habitat] * len(habitat_sb_data),
                                name=habitat + ' SB',
                                side='negative',
                                pointpos=-pointpos,
                                line_color=colors[habitat + '_SB'],
                                width=0.5,
                                jitter=0.2))  # Уменьшенная величина дрожи

        # Добавляем виолончель для NB
        fig.add_trace(go.Violin(y=habitat_nb_data,
                                x=[habitat] * len(habitat_nb_data),
                                name=habitat + ' NB',
                                side='positive',
                                pointpos=pointpos,
                                line_color=colors[habitat + '_NB'],
                                width=0.5,
                                jitter=0.2))  # Уменьшенная величина дрожи

    # Обновляем раскладку графика
    fig.update_traces(meanline_visible=True,
                      points='all',  # Показываем все точки
                      jitter=0.2,  # Увеличиваем дрожь для лучшей видимости точек
                      scalemode='count')  # Масштабирование площади виолончели в соответствии с количеством

    fig.update_layout(
        title_text="Distribution of " + species + " across habitats and sites",
        violingap=0.1,  # Уменьшенный промежуток между виолончелями
        violingroupgap=0.05,  # Уменьшенный промежуток между группами виолончелей
        violinmode='group',  # Группируем виолончели для каждой категории
        xaxis_title="Habitat and Site",
        yaxis_title="Value"
        
    )

# xaxis={'categoryorder':'total descending'}

    # Отображаем график
    # fig.write_html("violin/ " + species.lower() + ".html")
    # fig.show()

    fig.write_image("vector/"+species.lower()+".svg")

