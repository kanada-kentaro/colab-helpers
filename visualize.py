import cufflinks as cf
import IPython
from IPython.display import display

def configure_plotly_browser_state():
    display(IPython.core.display.HTML('''
        <script src="/static/components/requirejs/require.js"></script>
        <script>
          requirejs.config({
            paths: {
              base: '/static/base',
              plotly: 'https://cdn.plot.ly/plotly-latest.min.js?noext',
            },
          });
        </script>
        '''))

def register_visualize_funcs():
    cf.set_config_file(offline=True, theme="white", offline_show_link=False)
    if not configure_plotly_browser_state in IPython.get_ipython().events.callbacks['pre_run_cell']:
        IPython.get_ipython().events.register('pre_run_cell', configure_plotly_browser_state)
