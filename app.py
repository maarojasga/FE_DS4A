from multiapp import MultiApp
from apps import uls, exportaciones, home, mapas


app = MultiApp()


# Add all your applications here
app.add_app("Home",home.app)
app.add_app("Maps", mapas.app)

# The main app
app.run()
