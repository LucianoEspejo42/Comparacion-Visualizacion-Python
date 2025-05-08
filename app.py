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

if __name__ == "__main__":
    app.run(debug=True)
