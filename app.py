from flask import Flask, render_template
import json
import io
import base64

# Matplotlib
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Plotly
import plotly
import plotly.graph_objs as go

# Bokeh
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import ColumnDataSource
from bokeh.resources import CDN

import os
import sys

# Inicializar la app Flask
app = Flask(__name__)

@app.route('/')
def index():
    """
    Genera y renderiza visualizaciones con Matplotlib, Plotly y Bokeh.
    Esta función crea tres tipos diferentes de visualizaciones:
    1. Un gráfico de Matplotlib, que se convierte a una imagen PNG codificada en base64 para incrustarla en HTML.
    2. Un gráfico de Plotly, que se serializa a JSON para renderizarse con Plotly.js en el navegador.
    3. Un gráfico de Bokeh, que se renderiza utilizando los componentes y recursos de Bokeh.
    Las visualizaciones generadas se pasan a la plantilla "index.html" para su renderización.
    Devuelve:
    str: Plantilla HTML renderizada con visualizaciones incrustadas.
    """
    # Datos
    x = [1, 2, 3, 4, 5]
    y = [10, 15, 13, 17, 22]

    # 1. Matplotlib (convertido a base64 para incrustar en HTML)
    fig_mpl, ax = plt.subplots(figsize=(10, 4))
    ax.plot(x, y, marker='o', linestyle='-', color='red', label='Datos')
    ax.set_title('Valores de prueba - Matplotlib')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.grid(True, color='lightgray')
    fig_mpl.patch.set_facecolor('white')
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)
    matplotlib_graph = base64.b64encode(buffer.getvalue()).decode('utf-8')
    matplotlib_url = f"data:image/png;base64,{matplotlib_graph}"
    plt.close(fig_mpl)

    # 2. Plotly (convertido a JSON para usar con Plotly.js en el navegador)
    x1 = [1, 2, 3, 4, 5]
    y1 = [11, 16, 14, 18, 23]

    x2 = [1, 2, 3, 4, 5]
    y2 = [8, 12, 9, 14, 19]

    fig_plotly = go.Figure()
    fig_plotly.add_trace(go.Scatter(x=x, y=y, mode='lines+markers', name='Conjunto 1', line=dict(color='red')))
    fig_plotly.add_trace(go.Scatter(x=x1, y=y1, mode='lines+markers', name='Conjunto 2', line=dict(color='blue')))
    fig_plotly.add_trace(go.Scatter(x=x2, y=y2, mode='lines+markers', name='Conjunto 3', line=dict(color='purple')))
    fig_plotly.update_traces(marker=dict(size=10), line=dict(width=2))
    fig_plotly.update_layout(
        title='Valores de prueba - Plotly',
        xaxis_title='X',
        yaxis_title='Y',
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(color='black'),
        height=400,
        xaxis=dict(gridcolor='lightgray', zerolinecolor='black', linecolor='black', mirror=True),
        yaxis=dict(gridcolor='lightgray', zerolinecolor='black', linecolor='black', mirror=True)
    )
    plotly_json = json.dumps(fig_plotly, cls=plotly.utils.PlotlyJSONEncoder)

    # 3. Bokeh
    source = ColumnDataSource(data=dict(x=x, y=y))
    p = figure(
        title="Valores de prueba - Bokeh",
        x_axis_label="X",
        y_axis_label="Y",
        width=900,
        height=400,
        background_fill_color="white",
        border_fill_color="white"
    )
    p.line('x', 'y', source=source, line_width=2, line_color="purple")
    p.circle('x', 'y', source=source, size=8, fill_color="purple", line_color="purple")
    p.xgrid.grid_line_color = "lightgray"
    p.ygrid.grid_line_color = "lightgray"
    p.xaxis.axis_line_color = "black"
    p.yaxis.axis_line_color = "black"
    p.outline_line_color = "black"
    bokeh_script, bokeh_div = components(p)
    bokeh_resources = CDN.render()

    return render_template(
        "index.html",
        matplotlib_url=matplotlib_url,
        plotly_json=plotly_json,
        bokeh_resources=bokeh_resources,
        bokeh_script=bokeh_script,
        bokeh_div=bokeh_div
    )

@app.route('/libreria/matplotlib')
def info_matplotlib():
    contenido_html = """
    <h2>¿Qué es?</h2>
    <p>Es la librería de visualización más antigua y estable de Python.</p>
    <p>Se usa para gráficos estáticos: líneas, barras, tortas, etc.</p>
    <p>Inspirada en MATLAB.</p>

    <h2>¿Cómo funciona?</h2>
    <p>Dibuja gráficos usando objetos tipo figura (Figure) y ejes (Axes).</p>
    <p>Por defecto, muestra gráficos en una ventana (si hay GUI), pero también se pueden guardar como imágenes (.png, .svg, etc.).</p>

    <h2>Fortalezas</h2>
    <ul>
        <li>Ideal para informes o PDFs (gráficos no interactivos).</li>
        <li>Compatible con LaTeX para ecuaciones matemáticas.</li>
    </ul>

    <h2>Limitaciones</h2>
    <ul>
        <li>No es interactiva (sin zoom ni hover).</li>
        <li>Menos atractiva visualmente comparada con otras opciones modernas.</li>
    </ul>

    <h2>¿Con qué tipos de gráfico puedo trabajar?</h2>
    <p>Matplotlib es la biblioteca más básica y de más bajo nivel, ideal para personalización completa.</p>

    <ul>
        <li>Líneas (<code>plot</code>)</li>
        <li>Barras (<code>bar</code>, <code>barh</code>)</li>
        <li>Histogramas (<code>hist</code>)</li>
        <li>Dispersión (<code>scatter</code>)</li>
        <li>Pastel (<code>pie</code>)</li>
        <li>Boxplot (<code>boxplot</code>)</li>
        <li>Gráficos de áreas (<code>stackplot</code>)</li>
        <li>Imágenes (<code>imshow</code>)</li>
        <li>Contornos (<code>contour</code>)</li>
        <li>Gráficos 3D (con <code>mpl_toolkits.mplot3d</code>)</li>
        <li>Subplots personalizados</li>
    </ul>
    """
    return render_template("libreria.html", nombre="Matplotlib", contenido_html=contenido_html)


@app.route('/libreria/plotly')
def info_plotly():
    contenido_html = """
    <h2>¿Qué es?</h2>
    <p>Una librería de gráficos interactivos, moderna y potente.</p>
    <p>Usa JavaScript (Plotly.js) por detrás, pero tiene API en Python.</p>

    <h2>¿Cómo funciona?</h2>
    <p>En Python generás un objeto <code>Figure</code> con trazas (Trace) como <code>Scatter</code>, <code>Bar</code>, etc.</p>
    <p>El objeto se serializa en JSON.</p>
    <p>Luego, en el navegador se usa Plotly.js para renderizar ese JSON.</p>

    <h2>Fortalezas</h2>
    <ul>
        <li>Interactivo: permite zoom, tooltips, selección, etc.</li>
        <li>Fácil de integrar en dashboards web (Dash, Flask, Jupyter).</li>
        <li>Gráficos 3D, mapas, animaciones.</li>
    </ul>

    <h2>Limitaciones</h2>
    <ul>
        <li>Necesita que el navegador tenga JS habilitado.</li>
        <li>Más pesado (en cuanto a recursos y tamaño de librerías).</li>
    </ul>

    <h2>¿Con qué tipo de gráficos puedo trabajar?</h2>
    <p>Plotly es interactiva y muy rica visualmente. Ideal para dashboards y análisis exploratorio.</p>

    <ul>
        <li>Líneas (<code>go.Scatter</code>)</li>
        <li>Dispersión (<code>go.Scatter</code>)</li>
        <li>Barras (<code>go.Bar</code>)</li>
        <li>Pastel (<code>go.Pie</code>)</li>
        <li>Histogramas (<code>go.Histogram</code>)</li>
        <li>Boxplot (<code>go.Box</code>)</li>
        <li>Violin (<code>go.Violin</code>)</li>
        <li>Mapas de calor (<code>go.Heatmap</code>)</li>
        <li>Subplots y gráficos combinados</li>
        <li>Gráficos 3D (<code>go.Scatter3d</code>, <code>go.Surface</code>)</li>
        <li>Mapas geográficos (<code>go.Choropleth</code>, <code>go.Scattergeo</code>)</li>
        <li>Gráficos de red (usando <code>scatter</code> con <code>mode='lines+markers'</code>)</li>
    </ul>
    """
    return render_template("libreria.html", nombre="Plotly", contenido_html=contenido_html)

@app.route('/libreria/bokeh')
def info_bokeh():
    contenido_html = """
    <h2>¿Qué es?</h2>
    <p>Librería de gráficos interactivos pensada para la web.</p>
    <p>Ideal para integrar visualizaciones en dashboards HTML.</p>

    <h2>¿Cómo funciona?</h2>
    <p>En Python se define una figura <code>figure()</code>, se agregan glyphs como <code>line</code>, <code>circle</code>, etc.</p>
    <p>Bokeh genera automáticamente HTML + JS.</p>
    <p>Se inserta en páginas HTML con <code>&lt;div&gt;</code> y <code>&lt;script&gt;</code>.</p>

    <h2>Fortalezas</h2>
    <ul>
        <li>Muy buena integración con Flask, Django, etc.</li>
        <li>Altamente personalizable.</li>
        <li>Interactividad en tiempo real si se conecta con <code>bokeh server</code>.</li>
    </ul>

    <h2>Limitaciones</h2>
    <ul>
        <li>La sintaxis puede ser más verbosa.</li>
        <li>No tiene tantos tipos de gráficos como Plotly.</li>
    </ul>

    <h2>¿Con qué tipo de gráficos puedo trabajar?</h2>
    <p>Bokeh es interactiva como Plotly, pero está más orientada a visualización web y streaming de datos.</p>

    <ul>
        <li>Líneas (<code>line</code>)</li>
        <li>Dispersión (<code>circle</code>, <code>scatter</code>)</li>
        <li>Barras (<code>vbar</code>, <code>hbar</code>)</li>
        <li>Histogramas (combinando <code>quad</code>)</li>
        <li>Boxplot (con <code>Whisker</code>, <code>BoxAnnotation</code>)</li>
        <li>Gráficos de áreas</li>
        <li>Gráficos con sliders y widgets</li>
        <li>Gráficos con zoom, pan, hover</li>
        <li>Subplots y layouts</li>
        <li>Mapas (con <code>tile_sources</code> o integración con <code>GeoJSONDataSource</code>)</li>
        <li>Streaming plots (para datos en tiempo real)</li>
    </ul>
    """
    return render_template("libreria.html", nombre="Bokeh", contenido_html=contenido_html)


if __name__ == "__main__":
    app.run(debug=True)
