import pandas as pd
import numpy as np
import datetime
import pickle
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


class Car(BaseModel):
    seller: str
    offerType: str
    abtest: str
    vehicleType: str
    yearOfRegistration: int
    gearbox: str
    powerPS: int
    model: str
    kilometer: int
    fuelType: str
    brand: str
    notRepairedDamage: str


@app.get("/cars_price", response_class=HTMLResponse)
async def price_cars(request: Request):
    cars_item = {"seller": ['privat', 'gewerblich'], "offerType": ['Angebot', 'Gesuch'], "abtest": ['test', 'control'],
                 "vehicleType": ['limousine', 'kleinwagen', 'kombi', 'bus', 'cabrio', 'coupe', 'suv', 'andere'],
                 "yearOfRegistration": 0, "gearbox": ['manuell', 'automatik'], "powerPS": 0, "model":
                     ['golf', 'andere', '3er', 'polo', 'corsa', 'astra', 'passat', 'a4', 'c_klasse', '5er', 'e_klasse',
                      'a3', 'a6', 'focus', 'fiesta', 'transporter', 'twingo', '2_reihe', 'fortwo', 'a_klasse', 'vectra',
                      '1er', 'mondeo', 'clio', 'touran', '3_reihe', 'punto', 'zafira', 'megane', 'ibiza', 'ka', 'lupo',
                      'x_reihe', 'octavia', 'cooper', 'fabia', 'clk', 'micra', 'caddy', '80', 'sharan', 'scenic',
                      'omega', 'slk', 'leon', 'laguna', 'civic', 'tt', '1_reihe', '6_reihe', 'i_reihe', 'galaxy',
                      'm_klasse', '7er', 'meriva', 'yaris', 's_klasse', 'mx_reihe', 'a5', 'kangoo', '911', 'b_klasse',
                      '500', 'tiguan', 'vito', 'escort', 'one', 'arosa', 'z_reihe', 'bora', 'colt', 'beetle',
                      'berlingo', 'sprinter', 'tigra', 'v40', 'transit', 'touareg', 'fox', 'swift', 'insignia', 'c_max',
                      'corolla', 'panda', 'seicento', 'sl', 'v70', '4_reihe', 'scirocco', '156', 'a1', 'primera',
                      'espace', 'grand', 'stilo', 'almera', 'a8', '147', 'avensis', 'qashqai', 'eos', 'c3', 'signum',
                      'c5', 'kaefer', 's_max', '5_reihe', 'q5', 'c4', 'matiz', 'ducato', 'aygo', 'agila', 'viano',
                      'getz', '601', '100', 'combo', 'carisma', 'cayenne', 'boxster', 'alhambra', 'cordoba', 'c2',
                      'superb', 'c1', 'kuga', 'forfour', 'rio', 'jetta', 'cuore', 'a2', 'altea', 'kadett', 'rav',
                      'picanto', 'sorento', 'm_reihe', 'accord', 'cr_reihe', 'up', 'toledo', 'voyager', 'q7', 'vivaro',
                      'xc_reihe', 'bravo', 'santa', 'doblo', 'logan', 'modus', 'verso', 'ptcruiser', 'cl', 'sportage',
                      'jazz', 'fusion', 'sandero', 'mustang', 'roomster', 'carnival', 'ceed', '6er', 'galant', 'v50',
                      'q3', 'tucson', 'lancer', 'auris', 'impreza', 'phaeton', 'glk', 'freelander', 'pajero', 'calibra',
                      'x_trail', 'jimny', '159', '850', 'ypsilon', 'spider', 'duster', 'clubman', 'yeti', 'c_reihe',
                      'cc', 'roadster', 'cherokee', 'x_type', 'g_klasse', 'captiva', 'v_klasse', 'wrangler', 'legacy',
                      's60', '300c', 'rx_reihe', 'defender', 'sirion', 'justy', 'forester', 'outlander', 'note', 'niva',
                      's_type', 'spark', 'r19', 'navara', 'cx_reihe', '900', 'aveo', 'antara', '90', 'discovery',
                      'juke', 'exeo', 'range_rover_sport', 'kalos', 'range_rover', 'citigo', 'lanos', 'mii',
                      'crossfire', 'range_rover_evoque', 'gl', 'nubira', 'move', 'lybra', '145', 'v60', 'croma',
                      'amarok', 'delta', 'terios', 'lodgy', '9000', 'charade', 'b_max', 'musa', '200', 'materia',
                      'kappa', 'samara', 'elefantino', 'i3', 'kalina', 'serie_2', 'rangerover', 'serie_3', 'serie_1',
                      'discovery_sport'],
                 "kilometer": 0, "fuelType": ['benzin', 'diesel', 'lpg', 'cng', 'hybrid', 'andere', 'elektro'],
                 "brand": ['volkswagen', 'bmw', 'opel', 'mercedes_benz', 'audi', 'ford', 'renault', 'peugeot', 'fiat',
                           'seat', 'mazda', 'skoda', 'smart', 'citroen', 'nissan', 'toyota', 'sonstige_autos',
                           'hyundai', 'mini', 'volvo', 'mitsubishi', 'honda', 'kia', 'alfa_romeo', 'suzuki', 'porsche',
                           'chevrolet', 'chrysler', 'dacia', 'jeep', 'daihatsu', 'subaru', 'land_rover', 'jaguar',
                           'trabant', 'daewoo', 'saab', 'rover', 'lancia', 'lada'],
                 "notRepairedDamage": ['nein', 'ja']}
    return templates.TemplateResponse(name="cars.html", context={"request": request, "cars_item": cars_item})


def load_model():
    print("loading model...")
    global __model
    with open("autos_price_model.pickle", 'rb') as f:
        __model = pickle.load(f)


@app.post("/cars_price/")
def model_pred(seller: str = Form(...), offerType: str = Form(...), abtest: str = Form(...),
               vehicleType: str = Form(...), yearOfRegistration: int = Form(...), gearbox: str = Form(...),
               powerPS: int = Form(...), model: str = Form(...), kilometer: int = Form(...), fuelType: str = Form(...),
               brand: str = Form(...), notRepairedDamage: str = Form(...)):
    car = Car(seller=seller, offerType=offerType, abtest=abtest, vehicleType=vehicleType,
              yearOfRegistration=yearOfRegistration, gearbox=gearbox, powerPS=powerPS, model=model, kilometer=kilometer,
              fuelType=fuelType, brand=brand, notRepairedDamage=notRepairedDamage)
    load_model()
    data_to_pred = pd.DataFrame(jsonable_encoder(car), index=[0])
    x = pd.DataFrame(np.zeros((1, __model.n_features_in_)), columns=__model.feature_names_in_)
    x['yearsOld'] = datetime.date.today().year - data_to_pred['yearOfRegistration']
    x['powerPS'] = data_to_pred['powerPS']
    x['kilometer'] = data_to_pred['kilometer']
    for col in ['seller', 'offerType', 'abtest', 'vehicleType', 'gearbox', 'model', 'fuelType', 'brand',
                'notRepairedDamage']:
        if data_to_pred[col].iloc[0] in x.columns:
            x[data_to_pred[col]] = 1
    return str(round(np.e ** __model.predict(x)[0], 2)) + "€"

