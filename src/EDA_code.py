#Importo las librerías necesarias.
import pandas as pd 
import numpy as np 
import seaborn as sns
import matplotlib.pyplot as plt 
import missingno as msno
import plotly.graph_objects as go 

#Importo el Dataset y le asigno el nombre pokemon.
pokemon = pd.read_csv('./data/pokemon.csv')

#Información del DataFrame. 
pokemon.info()

#Descripción de estadísticas generales.
pokemon.describe(include = 'all')

#La columna con el nombre '#' que corresponde a la posición en la Pokédex no me aporta nada.
pokemon.drop('#', axis='columns', inplace=True)

#Recuento de valores únicos.
pokemon.value_counts()

#Visual de Correlaciones(Heatmap). 
sns.heatmap(pokemon[['Total','HP','Attack','Defense','Sp. Atk','Sp. Def','Speed', 'Legendary','Generation']].corr(), annot=True, cmap="coolwarm", vmin=-1)
plt.title('(Heatmap)')
plt.show()

#Comprobación de valores nulos (hay bastantes en type 2)
pokemon.isnull().sum()

#Visualizo los valores nulos.
msno.matrix(pokemon)

#Le asigno una letra a los nulos de la columna tipo 2 para que no molesten.
pokemon['Type 2'].fillna('x', inplace=True)

#Visualizo los valores átipicos de las columnas 'Total', 'Attack', 'HP' y 'Defense'.
sns.boxplot(pokemon, y='Total')
plt.title('Valores átipicos en ataque')
plt.show()

sns.boxplot(pokemon, y='Attack')
plt.title('Valores átipicos en ataque')
plt.show()

sns.boxplot(pokemon, y='HP')
plt.title('Valores átipicos de vida')
plt.show()

#Preparo una función para una visualización de estilo videojuego que usaré más adelante.
def PokeFightfull(pokemon, *pokemons):
    def get_stats(df, name):
        poke = df[df["Name"] == name]
        if poke.empty:
            raise ValueError(f"Pokémon {name} no encontrado.")
        return [
            poke['HP'].values[0],
            poke['Attack'].values[0],
            poke['Defense'].values[0],
            poke['Sp. Atk'].values[0],
            poke['Sp. Def'].values[0],
            poke['Speed'].values[0],
            poke['HP'].values[0]
        ]

    traces = []
    for name in pokemons:
        trace = go.Scatterpolar(
            r=get_stats(pokemon, name),
            theta=['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed', 'HP'],
            fill='toself',
            name=name
        )
        traces.append(trace)

    layout = go.Layout(
        title="Pokémons' Performance",
        polar=dict(
            radialaxis=dict(visible=True)
        ),
        showlegend=True
    )

    fig = go.Figure(data=traces, layout=layout)
    fig.show()
    
#¿Cuántas generaciones hay?
pokemon['Generation'].nunique()

#¿Cuántos Pokémon por cada generación?
pokemon['Generation'].value_counts()

#Añado un estilo visual general.
sns.set_style('dark')

#Visualización 'count' por generación.
plt.figure(figsize=(15,10))
sns.countplot(x='Generation', data=pokemon, hue='Generation', palette='Paired', legend=False)
plt.title('Cantidad de Pokémon por generación')

plt.show()

#Selección de colores para diagrama de dispersión por generación.
palette_generation = {
    1: '#0865de',      
    2: '#08d8de',     
    3: '#de0859',       
    4: '#d108de',    
    5: '#de8d08',    
    6: '#272625',           
}

#Diagrama de dispersión para el análisis de las relaciones entre variables y su correlación por generación. 
sns.pairplot(pokemon, vars=['Total','Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed'], hue='Generation', palette=palette_generation)
plt.show()

#Numero de Pokémon Legendarios por generación.
plt.figure(figsize=(15,10))
sns.countplot(x='Generation', data=pokemon, hue='Legendary', palette='Paired')
plt.title('Numero de Pokémon Legendarios por generación')
plt.show()

#Los Pokémon más fuertes por generación.  
generation_best = pokemon.iloc[[163,268,426,552,711,796]].sort_values('Total',ascending=False)
generation_best

#Visualización de los pokémon más fuertes por generación.
sns.catplot(generation_best, x='Name', y='Total', palette='tab20',hue='Name', kind="bar",height = 15) 
plt.title('Pokémon con el total más alto por generación',fontsize=15)
plt.show()
sns.catplot(generation_best, x='Name', y='Attack', hue='Name', palette='tab20', kind="bar",height = 15)
plt.title('Pokémon con el ataque más alto por generación' , fontsize=15)
plt.show()
sns.catplot(generation_best, x='Name', y='Defense', hue='Name', palette='tab20', kind="bar",height = 15)
plt.title('Pokémon con la defensa más alta por generación', fontsize=15)
plt.show()
sns.catplot(generation_best, x='Name', y='HP', hue='Name', palette='tab20', kind="bar",height = 15)
plt.title('Pokémon con la vida más alta por generación', fontsize=15)
plt.show()

#Comparativa de estadisticas de los Pokémon seleccionados.
PokeFightfull(pokemon, 'MewtwoMega Mewtwo X', 'TyranitarMega Tyranitar', 'RayquazaMega Rayquaza', 'Arceus', 'KyuremBlack Kyurem', 'DiancieMega Diancie')
plt.show()

#¿Cuántos tipos de Pokémon existen?
pokemon['Type 1'].nunique()

#¿Cuántos Pokémon por tipo existen?
pokemon['Type 1'].value_counts()

#Creo la variable de control que usaré para ordenar algunos visuales.
type_counts = pokemon['Type 1'].value_counts()

#Visualizacion del numero de Pokémon por tipo.
plt.figure(figsize=(15,10))
sns.countplot(x='Type 1',hue='Type 1' , order=type_counts.index , data=pokemon, palette=['#7ec63c','#f0560f','#3ba7fa','#aab31f','#d5cec8','#9e58a0','#f8bc16','#dabe6a','#f9bef8','#944526','#ef4681','#c1a961','#6f72bd','#7ddbf7','#7059d8','#584537','#9ea0af','#8fa3ec'])
plt.title('Pokémon por tipo')
plt.xticks(rotation = 45)
plt.show()


#Visualización del número de Pokémon por tipo en formato de tarta.
plt.figure(figsize=(15,10))
plt.pie(pokemon['Type 1'].value_counts(), labels = pokemon['Type 1'].value_counts().index)
my_circle=plt.Circle( (0,0),
                     0.7, # Grosor del donut
                     color='white')
p=plt.gcf()
p.gca().add_artist(my_circle);
plt.show()

#Diagrama de dispersión para el análisis de las relaciones entre variables y su correlación por tipo. 
sns.pairplot(pokemon, vars=['Total','Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed'], hue='Type 1', palette='tab20')
plt.show()

#Distribución de tipos de Pokémon por generación.
plt.figure(figsize=(15,10))
plt.subplot(2, 1, 1)
sns.countplot(data=pokemon, x='Type 1', order=type_counts.index,hue='Generation', palette='tab20', linewidth=0, )
plt.title('Distribución de tipos de Pokémon por generación')
plt.xlabel('Type 1')
plt.ylabel('Count')

#Distribución de tipos de Pokémon por estado legendario.
plt.subplot(2, 1, 2)
sns.countplot(data=pokemon, x='Type 1',order=type_counts.index , hue='Legendary', palette='hot_r', linewidth=0, )
plt.title('Distribución de tipos de Pokémon por estado legendario')
plt.xlabel('Type 1')
plt.ylabel('Count')


plt.tight_layout()
plt.show()

#Creo las variables para el comando 'order'.
attack_order = pokemon.groupby('Type 1')['Attack'].mean().sort_values(ascending=False).index
defense_order = pokemon.groupby('Type 1')['Defense'].mean().sort_values(ascending=False).index
HP_order = pokemon.groupby('Type 1')['HP'].mean().sort_values(ascending=False).index

#Distribución de Pokémon por tipo con indicadores de fuerza, vida y defensa.
plt.figure(figsize=(15,10))
sns.catplot(pokemon, x='Type 1', hue='Type 1', y='Attack',errorbar=None, order=attack_order, palette='Set2', kind="bar", height = 15) 
plt.title('Distribución de tipos de Pokémon por fuerza')

sns.catplot(pokemon, x='Type 1', hue='Type 1', y='Defense', errorbar = None, order=defense_order, palette='Set2', kind="bar", height = 15) 
plt.title('Distribución de tipos de Pokémon por defensa')

sns.catplot(pokemon, x='Type 1', hue='Type 1', y='HP', palette='Set2', errorbar=None, order = HP_order, kind="bar", height = 15) 
plt.title('Distribución de tipos de Pokémon por vida')
plt.show()

#Visualización de los valores átipicos por tipo.
plt.figure(figsize=(15,8)) 
sns.boxplot(x = pokemon['Type 1'],y = pokemon['Total'])
plt.title('Visualización de los valores átipicos por tipo')
plt.show()

#¿Cual es el pokemon más fuerte por tipo y sus estadisticas? 
best_type = pokemon.loc[pokemon.groupby('Type 1')['Attack'].idxmax(), ['Type 1','Total','Name','HP','Attack','Defense','Sp. Atk','Sp. Def','Speed']]
best_type 

#Visualización: ¿Cual es el pokemon con el total más alto por tipo? 
order_total = best_type.groupby('Name')['Total'].mean().sort_values(ascending=False).index
plt.figure(figsize=(15,10))
sns.catplot(best_type, x='Name', y='Total', hue='Name',order= order_total, palette='Set2', kind="bar", height = 15) 
plt.xticks(rotation = 90)
plt.title('Distribución de los Pokémon más fuertes por tipo midiendo el total')
plt.show()

#Visualización: ¿Cual es el pokemon con el ataque más fuerte por tipo? 
order_attack = best_type.groupby('Name')['Attack'].mean().sort_values(ascending=False).index
plt.figure(figsize=(15,10))
sns.catplot(best_type, x='Name', y='Attack', hue='Name', order= order_attack , palette='Set2', kind="bar", height = 15) 
plt.xticks(rotation = 90)
plt.title('Distribución de los Pokémon más fuertes por tipo midiendo el ataque')
plt.show()

#Visualización: ¿Cual es el pokemon con la defensa más alta por tipo? 
order_defense = best_type.groupby('Name')['Defense'].mean().sort_values(ascending=False).index
plt.figure(figsize=(15,10))
sns.catplot(best_type, x='Name', y='Defense', hue='Name', order=order_defense, palette='Set2', kind="bar", height = 15) 
plt.xticks(rotation = 90)
plt.title('Distribución de los Pokémon más fuertes por tipo midiendo la defensa')
plt.show()

#Visualización: ¿Cual es el pokemon con más vida por tipo? 
order_hp = best_type.groupby('Name')['HP'].mean().sort_values(ascending=False).index
plt.figure(figsize=(15,10))
sns.catplot(best_type, x='Name',hue='Name', y='HP',order=order_hp, palette='Set2', kind="bar", height = 15) 
plt.xticks(rotation = 90)
plt.title('Distribución de los Pokémon más fuertes por tipo midiendo su vida')
plt.show()

#Son los Pokémon más fuertes de cada tipo legendarios o no?
best_type_legend = pokemon.loc[pokemon.groupby('Type 1')['Attack'].idxmax(), ['Type 1','Total','Name','HP','Attack','Defense','Sp. Atk','Sp. Def','Speed','Legendary']]
best_type_legend
plt.figure(figsize=(15,10))
plt.subplot(2, 1, 2)
sns.countplot(data=best_type_legend, x='Name', hue='Legendary', palette='hot_r', )
plt.xticks(rotation = 90)
plt.title('Estado legendario')
plt.xlabel(' ')
plt.ylabel('')
plt.show()

#Comparativa visual estilo video juego de las estadisticas de los Pokémon más fuertes por tipo. 
PokeFightfull(
    pokemon, 
    'HeracrossMega Heracross', 
    'AbsolMega Absol',
    'RayquazaMega Rayquaza',
    'Electivire',
    'Xerneas',
    'LucarioMega Lucario',
    'BlazikenMega Blaziken',
    'TornadusIncarnate Forme',
    'BanetteMega Banette',
    'AbomasnowMega Abomasnow',
    'GroudonPrimal Groudon',
    'Mamoswine',
    'Slaking',
    'Toxicroak',
    'MewtwoMega Mewtwo X',
    'Rampardos',
    'AegislashBlade Forme',
    'GyaradosMega Gyarados'
)
plt.show()

#Numero total de Pokémon
len(pokemon)

#Grupo con los mejores de cada estadistica.
best_of_best = pokemon.iloc[[426,261,163,333,431]]

#¿De los mejores de cada estadística cuales son legendarios?
plt.figure(figsize=(15,10))
plt.subplot(2, 1, 2)
sns.countplot(data=best_of_best, x='Name', hue='Legendary', palette='hot_r', )
plt.xticks(rotation = 90)
plt.title('Estado legendario')
plt.xlabel(' ')
plt.ylabel('')
plt.show()

#¿De que generación son los mejores de cada estadistica?
plt.figure(figsize=(15,10))
plt.subplot(2, 1, 1)
sns.countplot(data=best_of_best, x='Name', hue='Generation', palette='Set2', linewidth=0, alpha=1)
plt.title('Distribución de tipos de Pokémon por generación')
plt.xticks(rotation = 90)
plt.xlabel('Type 1')
plt.ylabel('Count')
plt.show()

#Comparativa visual estilo video juego de las estadisticas del grupo Best of best.
PokeFightfull(pokemon, 'RayquazaMega Rayquaza', 'Blissey','MewtwoMega Mewtwo X', 'AggronMega Aggron','DeoxysSpeed Forme')
plt.show()

#Selección de los Pokémon iniciales para el estudio.
best_ini = pokemon.iloc[[9,4,0]]

#Visualización por Total.
sns.catplot(best_ini, x= 'Name', hue='Name',legend=False, y='Total', palette=['#41bee6', '#d51717', '#79f5bf'], kind="bar", height = 15) 
plt.title('Distribución de Pokémon inicales por Suma total')

#Visualización por fuerza.
sns.catplot(best_ini, x= 'Name', hue='Name',legend=False, y='Attack', palette=['#41bee6', '#d51717', '#79f5bf'], kind="bar", height = 15) 
plt.title('Distribución de Pokémon inicales por fuerza')

#Visualización por vida.
sns.catplot(best_ini, x= 'Name', hue='Name',legend=False, y='HP', palette=['#41bee6', '#d51717', '#79f5bf'], kind="bar", height = 15) 
plt.title('Distribución de Pokémon inicales por vida')

#Visualización por defensa.
sns.catplot(best_ini, x= 'Name', hue='Name',legend=False, y='Defense', palette=['#41bee6', '#d51717', '#79f5bf'], kind="bar", height = 15) 
plt.title('Distribución de Pokémon inicales por defensa') 

#Visualización por velocidad.
sns.catplot(best_ini, x= 'Name', hue='Name',legend=False, y='Speed', palette=['#41bee6', '#d51717', '#79f5bf'], kind="bar", height = 15) 
plt.title('Distribución de Pokémon inicales por velocidad')

#Visualización por SP.Atk.
sns.catplot(best_ini, x= 'Name', hue='Name',legend=False, y='Sp. Atk', palette=['#41bee6', '#d51717', '#79f5bf'], kind="bar", height = 15) 
plt.title('Distribución de Pokémon inicales por ataque especial')

#Visualización por Sp. Def.
sns.catplot(best_ini, x= 'Name', hue='Name',legend=False, y='Sp. Def', palette=['#41bee6', '#d51717', '#79f5bf'], kind="bar", height = 15) 
plt.title('Distribución de Pokémon inicales por ataque especial')
plt.show()

#Visualización estadisticas tipo video juego. 
PokeFightfull(pokemon, 'Squirtle', 'Charmander', 'Bulbasaur')
plt.show()

#Comparativa visual contra el mejor y el peor electrico.
PokeFightfull(pokemon, 'Pikachu', 'AmpharosMega Ampharos', 'Pichu')
plt.show()

#Comparativa visual Pikachu vs los demás electricos.
electric_pokemon = pokemon[pokemon['Type 1'] == 'Electric']
electric_pokemon['pikachu'] = electric_pokemon['Name'].apply(lambda x: 'Pikachu' if x == 'Pikachu' else 'Others')
order_pika = electric_pokemon.groupby('Name')['Total'].mean().sort_values(ascending=True).index
sns.catplot(electric_pokemon, x= 'Name', hue='pikachu',order=order_pika, legend=False, y='Total', palette=['#f4ee2d', '#d51717'], kind="bar", height = 15) 
plt.xticks(rotation = 90)
plt.title('Pikachu vs todos los Pokémon eléctricos') 
plt.show()

sns.pairplot(electric_pokemon, vars=['Total', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed'],
             hue='pikachu', palette=['#41bee6', '#d51717'])
plt.show() 


