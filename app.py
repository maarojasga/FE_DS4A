from multiapp import MultiApp
from apps import uls, home, mapas, layout, table


app = MultiApp()


# Add all your applications here
app.add_app("Home",home.app)
app.add_app("Maps", mapas.app)
app.add_app("Layout", layout.app)
app.add_app("Table", table.app)


# The main app
app.run()
