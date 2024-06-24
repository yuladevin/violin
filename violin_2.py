import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

# Загрузка датафрейма
df = pd.read_csv("tables/Lin_data.xlsx")



# Определение цветов для каждой комбинации Habitat и Site
colors = {
    'L_SB': 'lightgreen',
    'L_NB': 'green',
    'SIM_SB': 'yellow',
    'SIM_NB': 'orange',
    'SOM_SB': 'pink',
    'SOM_NB': 'red'
}

# Получаем уникальные среды обитания и виды
unique_habitats = df['Habitat'].unique()
species_columns = df.columns[3:11]  # Используйте фактические индексы ваших видов

# Создаем сетку субплотов для каждого вида
num_species = len(species_columns)
# fig = make_subplots(rows=num_species, cols=1, shared_xaxes=True)


# Создайте сетку субплотов
fig = make_subplots(rows=num_species, cols=1, subplot_titles=species_columns)



for i, species in enumerate(species_columns, start=1):
    for habitat in unique_habitats:
        # Фильтруем данные для каждой среды обитания и каждого сайта
        habitat_data = df[df['Habitat'] == habitat]
        habitat_sb_data = habitat_data[habitat_data['Site'] == 'SB'][species]
        habitat_nb_data = habitat_data[habitat_data['Site'] == 'NB'][species]

        # Добавляем виолончель для SB
        fig.add_trace(go.Violin(y=habitat_sb_data,
                                x=[habitat] * len(habitat_sb_data),
                                name=f'{habitat} SB',
                                side='negative',
                                line_color=colors[f'{habitat}_SB'],
                                showlegend=(i == 1)),  # Показываем легенду только для первого графика
                          row=i, col=1)

        # Добавляем виолончель для NB
        fig.add_trace(go.Violin(y=habitat_nb_data,
                                x=[habitat] * len(habitat_nb_data),
                                name=f'{habitat} NB',
                                side='positive',
                                line_color=colors[f'{habitat}_NB'],
                                showlegend=False),  # Скрываем легенду для остальных графиков
                          row=i, col=1)

# Обновляем раскладку графика
fig.update_layout(height=300 * num_species, width=1000, title_text="Distribution of Species across Habitats and Sites")
fig.update_xaxes(title_text="Habitat and Site", row=num_species, col=1)  # Добавляем название оси X только к нижнему графику

# Отображаем график
fig.show()

