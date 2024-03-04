from flask import Flask, render_template, request, redirect, session,url_for
import pandas as pd
import copy

app = Flask(__name__)
app.secret_key = 'your_secret_key'

df = pd.read_csv('./clustersAtractivoJuntos_variablesWeb.csv') 
df_extra = pd.read_csv('./distritosAtractivoJuntos_variablesWeb.csv') 

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/select_group',methods=['GET'])
def select_group():
    return render_template('select_group.html')

@app.route('/select_importance', methods=['POST'])
def select_importance():
    global filtered_df
    groups = request.form.getlist('group')
    df_copy = copy.deepcopy(df)
    filtered_df = df_copy[df_copy['grupo'].isin([int(group) for group in groups])]
    madrid_option = request.form.get('madrid')
    if madrid_option:
        return redirect('/madrid')
    else:
        return render_template('educationMun.html', groups=groups)
    
@app.route('/madrid')
def madrid():
    return render_template('educationDis.html')

@app.route('/final_results_extra_education', methods=['POST'])
def final_results_extra_education():
    session['private_education'] = int(request.form['private_education'])
    session['public_education'] = int(request.form['public_education'])
    session['libraries'] = int(request.form['libraries'])    
    session['foreigner_student'] = int(request.form['foreigner_student'])
    session['mayores'] = int(request.form['mayores'])
    session['centros'] = int(request.form['centros']) 
    session['otherCentros'] = int(request.form['otherCentros']) 
    return redirect(url_for('final_results_extra_security'))

@app.route('/final_results_extra_security', methods=['POST', 'GET'])
def final_results_extra_security():
    if request.method == 'POST':
        session['bicis'] = int(request.form['bicis'])
        session['metro'] = int(request.form['metro'])
        session['accidentes'] = int(request.form['accidentes'])
        session['detenidos'] = int(request.form['detenidos'])
        session['policia'] = int(request.form['policia'])
        return redirect(url_for('final_results_extra_population'))
    else:
        return render_template('securityDis.html')

@app.route('/final_results_extra_population', methods=['POST', 'GET'])
def final_results_extra_population():
    if request.method == 'POST':
        session['density'] = int(request.form['density'])
        session['foreigners'] = int(request.form['foreigners'])
        session['young'] = int(request.form['young'])    
        session['highEduc'] = int(request.form['highEduc'])
        session['women'] = int(request.form['women'])
        return redirect(url_for('final_results_extra_realestate'))
    else:
        return render_template('populationDis.html')

@app.route('/final_results_extra_realestate', methods=['POST', 'GET'])
def final_results_extra_realestate():
    if request.method == 'POST':
        session['good_houses'] = int(request.form['good_houses'])
        session['houses'] = int(request.form['houses'])
        session['size'] = int(request.form['size'])
        session['general_features'] = int(request.form['general_features'])
        session['new_development'] = int(request.form['new_development'])    
        session['price'] = int(request.form['price'])
        return redirect(url_for('final_results_extra'))
    else:
        return render_template('realEstateDis.html')
    
@app.route('/final_results_extra', methods=['POST', 'GET'])
def final_results_extra():
    if request.method == 'POST':
        session['sport_greenareas'] = int(request.form['sport_greenareas'])
        session['espectaculos'] = int(request.form['espectaculos'])
        session['residuos'] = int(request.form['residuos'])
        session['paro'] = int(request.form['paro'])
        session['locales'] = int(request.form['locales'])  
        
        private_education = session.get('private_education')
        public_education = session.get('public_education')
        libraries = session.get('libraries')
        foreigner_student = session.get('foreigner_student')
        
        density = session.get('density')
        foreigners = session.get('foreigners')
        young = session.get('young')
        highEduc = session.get('highEduc')
        women = session.get('women')
        
        good_houses = session.get('good_houses')
        houses = session.get('houses')
        size = session.get('size')
        general_features = session.get('general_features')
        new_development = session.get('new_development')
        price = session.get('price')
        
        centros = session.get('centros')
        mayores = session.get('mayores')
        otherCentros = session.get('otherCentros')
        
        bicis = session.get('bicis')
        metro = session.get('metro')
        accidentes = session.get('accidentes')
        detenidos = session.get('detenidos')
        policia = session.get('policia')
        
        locales = session.get('locales')
        paro = session.get('paro')
        espectaculos = session.get('espectaculos')
        residuos = session.get('residuos') 
        sport_greenareas = session.get('sport_greenareas')
        
        sumImportances = (2 * private_education + 2 * public_education + libraries + 2 * foreigner_student 
                         + density + foreigners + young + 3 * highEduc + women + 2 * good_houses + houses + 4 * size + 3 * general_features + 2 * new_development + 2 * price + 2 * centros + 4 * mayores + 3 * otherCentros + metro + 2 * bicis + accidentes + detenidos + policia + paro + locales + 2 * espectaculos + residuos + 5 * sport_greenareas)
        
        df_extra['weighted_sum'] = 0
    
        #Education
        df_extra['weighted_sum'] += private_education * df_extra['centrosPrivadoporAlumno_100']
        df_extra['weighted_sum'] += private_education * df_extra['centrosPrivadoporAlumnoExtr_100']
        df_extra['weighted_sum'] += public_education * df_extra['centrosPublicoporAlumno_100']
        df_extra['weighted_sum'] += public_education * df_extra['centrosPublicoporAlumnoExtr_100']
        df_extra['weighted_sum'] += libraries * df_extra['bibliotecas_100']
        df_extra['weighted_sum'] += foreigner_student * df_extra['porcAlumnoExtranjero']
        df_extra['weighted_sum'] += foreigner_student * df_extra['porcApoyoEducativo']
        
        #Security
        df_extra['weighted_sum'] += accidentes * df_extra['Atestados/partes de accidentes de tráfico confeccionados']
        df_extra['weighted_sum'] += detenidos * df_extra['detenidos_100']
        df_extra['weighted_sum'] += policia * df_extra['sumaIntervecniones']
        
        #Population and general
        df_extra['weighted_sum'] += density * df_extra['Población densidad (hab./Ha.)']
        df_extra['weighted_sum'] += women * df_extra['frac_mujeres']
        df_extra['weighted_sum'] += foreigners * df_extra['frac_extranjeros']
        df_extra['weighted_sum'] += young * df_extra['frac_young']
        df_extra['weighted_sum'] += highEduc * df_extra['frac_HighEduc']
        df_extra['weighted_sum'] += sport_greenareas * df_extra['zonasVerdes(ha)']
        df_extra['weighted_sum'] += sport_greenareas * df_extra['superficieDeportiva(m2)']
        df_extra['weighted_sum'] += sport_greenareas * df_extra['centrosDeportivos_100']
        df_extra['weighted_sum'] += sport_greenareas * df_extra['instalacionesDeportivasBasicas_100']
        df_extra['weighted_sum'] += sport_greenareas * df_extra['piscinasCubiertas_100']
        df_extra['weighted_sum'] += espectaculos * df_extra['espaciosCulturales_100']
        df_extra['weighted_sum'] += espectaculos * df_extra['espectaculos_100']
        df_extra['weighted_sum'] += residuos * df_extra['residuos(kg/hab/dia)']
        
        #Housing
        df_extra['weighted_sum'] += new_development * df_extra['añoMedioConstruccion']
        df_extra['weighted_sum'] += good_houses * df_extra['Viviendas en estado bueno']
        df_extra['weighted_sum'] += good_houses * df_extra['viviendasMalEstado']
        df_extra['weighted_sum'] += houses * df_extra['viviendas_habitante']
        df_extra['weighted_sum'] += size * df_extra['size']
        df_extra['weighted_sum'] += size * df_extra['rooms']
        df_extra['weighted_sum'] += size * df_extra['bathrooms']
        df_extra['weighted_sum'] += general_features * df_extra['hasLift']
        df_extra['weighted_sum'] += general_features * df_extra['parkingSpace']
        df_extra['weighted_sum'] += general_features * df_extra['pisoBajo']
        df_extra['weighted_sum'] += new_development * df_extra['newDevelopment']
        df_extra['weighted_sum'] += size * df_extra['propertyType']
        df_extra['weighted_sum'] += price * df_extra['priceByArea_x']
        df_extra['weighted_sum'] += price * df_extra['price']
        
        #Sanity
        df_extra['weighted_sum'] += centros * df_extra['CentrosSalud_100']
        df_extra['weighted_sum'] += centros * df_extra['HospitalesClinicasSanatorios_100']
        df_extra['weighted_sum'] += mayores * df_extra['CentrosMayores_100']
        df_extra['weighted_sum'] += mayores * df_extra['ServiciosSociales_100']
        df_extra['weighted_sum'] += mayores * df_extra['AuxHogar_100']
        df_extra['weighted_sum'] += mayores * df_extra['socioCentrosMayores_100']
        df_extra['weighted_sum'] += otherCentros * df_extra['drogas/especialidades_100']
        df_extra['weighted_sum'] += otherCentros * df_extra['CentrosSaludMental_100']
        df_extra['weighted_sum'] += otherCentros * df_extra['CentrosAlzheimer_100']
        
        #Transport
        df_extra['weighted_sum'] += bicis * df_extra['estBici_100']
        df_extra['weighted_sum'] += bicis * df_extra['numBici_100']
        df_extra['weighted_sum'] += metro * df_extra['metro_100']
        
        #Work
        df_extra['weighted_sum'] += paro * df_extra['paro_100']
        df_extra['weighted_sum'] += highEduc * df_extra['crecimientoRentaPC']
        df_extra['weighted_sum'] += highEduc * df_extra['rentaMedia']
        df_extra['weighted_sum'] += locales * df_extra['localesAbiertos_100']
        
        if sumImportances == 0:
            df_extra['weighted_sum'] = (df_extra.iloc[:, 1:16].sum(axis=1) + df_extra.iloc[:, 17:24].sum(axis=1) + df_extra.iloc[:, 25:31].sum(axis=1) + df_extra.iloc[:, 33:61].sum(axis=1)) / 56
        else:
            df_extra['weighted_sum'] = round(df_extra['weighted_sum'] / sumImportances , 2)
            
        df_extra['priceByArea_y'] = round(df_extra['priceByArea_y'] , 2)
        try:
            df_extra['Número Habitantes_y'] = (df_extra['Número Habitantes_y']).astype(int)
            df_extra['Número Habitantes_y'] = df_extra['Número Habitantes_y'].map('{:,}'.format)
            df_extra['Número Habitantes_y'] = df_extra['Número Habitantes_y'].str.replace(',', '.')
            df_extra['posicionVulnerabilidad_y'] = (df_extra['posicionVulnerabilidad_y']).astype(int)
        except: 
            pass
        
        sorted_df = df_extra.sort_values(by='weighted_sum', ascending=False)
        sorted_df = sorted_df.head(10)
        return render_template('final_results_extra.html', data=sorted_df[['distrito', 'weighted_sum','priceByArea_y','Número Habitantes_y','posicionVulnerabilidad_y']]) 
    else:
        return render_template('economicDynamismDis.html')


@app.route('/final_results_education', methods=['POST'])
def final_results_education():
    session['private_education'] = int(request.form['private_education'])
    session['public_education'] = int(request.form['public_education'])
    session['libraries'] = int(request.form['libraries'])    
    session['centros'] = int(request.form['centros'])
    session['pharmacy'] = int(request.form['pharmacy'])
    session['otherCentros'] = int(request.form['otherCentros']) 
    return redirect(url_for('final_results_airquality'))

@app.route('/final_results_airquality', methods=['POST', 'GET'])
def final_results_airquality():
    if request.method == 'POST':
        session['air_quality'] = int(request.form['air_quality'])
        session['temperature'] = int(request.form['temperature'])
        session['distance'] = int(request.form['distance'])
        session['vehicles'] = int(request.form['vehicles'])
        session['stations'] = int(request.form['stations'])
        return redirect(url_for('final_results_population'))
    else:
        return render_template('airQualityMun.html')

@app.route('/final_results_population', methods=['POST', 'GET'])
def final_results_population():
    if request.method == 'POST':
        session['density'] = int(request.form['density'])
        session['foreigners'] = int(request.form['foreigners'])
        session['young'] = int(request.form['young'])    
        session['highEduc'] = int(request.form['highEduc'])
        return redirect(url_for('final_results_realestate'))
    else:
        return render_template('populationMun.html')

@app.route('/final_results_realestate', methods=['POST', 'GET'])
def final_results_realestate():
    if request.method == 'POST':
        session['urban_units'] = int(request.form['urban_units'])
        session['size'] = int(request.form['size'])
        session['general_features'] = int(request.form['general_features'])
        session['new_development'] = int(request.form['new_development'])    
        session['price'] = int(request.form['price'])
        return redirect(url_for('final_results_economy'))
    else:
        return render_template('realEstateMun.html')

@app.route('/final_results_economy', methods=['POST', 'GET'])
def final_results_economy():
    if request.method == 'POST':
        session['trabajadoresZona'] = int(request.form['trabajadoresZona'])
        session['paro'] = int(request.form['paro'])
        session['pension'] = int(request.form['pension'])
        session['organizations'] = int(request.form['organizations'])

        private_education = session.get('private_education')
        public_education = session.get('public_education')
        libraries = session.get('libraries')
        
        air_quality = session.get('air_quality')
        temperature = session.get('temperature')
        
        density = session.get('density')
        foreigners = session.get('foreigners')
        young = session.get('young')
        highEduc = session.get('highEduc')
        
        urban_units = session.get('urban_units')
        size = session.get('size')
        general_features = session.get('general_features')
        new_development = session.get('new_development')
        price = session.get('price')
        
        centros = session.get('centros')
        pharmacy = session.get('pharmacy')
        otherCentros = session.get('otherCentros')
        
        distance = session.get('distance')
        vehicles = session.get('vehicles')
        stations = session.get('stations')
        
        trabajadoresZona = session.get('trabajadoresZona')
        paro = session.get('paro')
        pension = session.get('pension')
        organizations = session.get('organizations')
        
        sumImportances = (3 * private_education + 3 * public_education + 3 * libraries + 6 * air_quality 
                        + 3 * temperature + density + foreigners + young + 2 * highEduc + 2 * urban_units
                        + 3 * general_features + new_development + 2 * price + centros + pharmacy + 5 * otherCentros
                        + distance + 2 * vehicles + 2 * stations + 3 * trabajadoresZona + paro + pension + organizations)
        
        if size != 0:
            sumImportances += 8 * size + (10 - size)
        
        filtered_df['weighted_sum'] = 0 
        
        #Education
        filtered_df['weighted_sum'] += private_education * filtered_df['escuelas/100_alumnos_priv']
        filtered_df['weighted_sum'] += private_education * filtered_df['unidadEsc/100_alumnos_priv']
        filtered_df['weighted_sum'] += private_education * filtered_df['profesores/100_alumnos_priv']
        filtered_df['weighted_sum'] += public_education * filtered_df['escuelas/100_alumnos_pub']
        filtered_df['weighted_sum'] += public_education * filtered_df['unidadEsc/100_alumnos_pub']
        filtered_df['weighted_sum'] += public_education * filtered_df['profesores/100_alumnos_pub']
        filtered_df['weighted_sum'] += libraries * filtered_df['bibliotecas/100_alumnos']
        filtered_df['weighted_sum'] += libraries * filtered_df['idiomas/10_alumnos']
        filtered_df['weighted_sum'] += libraries * filtered_df['actividades/10_alumnos']
        
        #Air quality
        filtered_df['weighted_sum'] += air_quality * filtered_df['Magnitud6']
        filtered_df['weighted_sum'] += air_quality * filtered_df['Magnitud7']
        filtered_df['weighted_sum'] += air_quality * filtered_df['Magnitud8']
        filtered_df['weighted_sum'] += air_quality * filtered_df['Magnitud10']
        filtered_df['weighted_sum'] += air_quality * filtered_df['Magnitud12']
        filtered_df['weighted_sum'] += air_quality * filtered_df['Magnitud14']
        filtered_df['weighted_sum'] += temperature * filtered_df['Magnitud83']
        filtered_df['weighted_sum'] += temperature * filtered_df['Magnitud88']
        filtered_df['weighted_sum'] += temperature * filtered_df['Magnitud89']
        
        #Population and general
        filtered_df['weighted_sum'] += density * filtered_df['densidad']
        filtered_df['weighted_sum'] += foreigners * filtered_df['frac_extranjeros']
        filtered_df['weighted_sum'] += young * filtered_df['frac_young']
        filtered_df['weighted_sum'] += highEduc * filtered_df['frac_HighEduc']
        
        #Housing
        filtered_df['weighted_sum'] += urban_units * filtered_df['unidadesUrbanasResidenciales']
        filtered_df['weighted_sum'] += urban_units * filtered_df['numHouses']
        filtered_df['weighted_sum'] += general_features * filtered_df['hasLift']
        filtered_df['weighted_sum'] += general_features * filtered_df['parkingSpace']
        filtered_df['weighted_sum'] += general_features * filtered_df['pisoBajo']
        filtered_df['weighted_sum'] += new_development * filtered_df['newDevelopment']
        filtered_df['weighted_sum'] += price * filtered_df['priceByArea_x']
        filtered_df['weighted_sum'] += price * filtered_df['price']
        filtered_df['weighted_sum'] += size * filtered_df['size']
        filtered_df['weighted_sum'] += size * filtered_df['rooms']
        filtered_df['weighted_sum'] += size * filtered_df['bathrooms']
        filtered_df['weighted_sum'] += size * filtered_df['familiares']
        filtered_df['weighted_sum'] += size * filtered_df['antiguedadFamiliares']
        filtered_df['weighted_sum'] += size * filtered_df['superficieFamiliares']
        if size != 0:
            filtered_df['weighted_sum'] += (10 - size) * filtered_df['1-3p']
        filtered_df['weighted_sum'] += size * filtered_df['4+p']
        filtered_df['weighted_sum'] += size * filtered_df['propertyType']

        
        #Sanity
        filtered_df['weighted_sum'] += centros * filtered_df['centros_100']
        filtered_df['weighted_sum'] += pharmacy * filtered_df['farmacias_100']
        filtered_df['weighted_sum'] += otherCentros * filtered_df['centrosSociales_10']
        filtered_df['weighted_sum'] += otherCentros * filtered_df['clinicaDental_10']
        filtered_df['weighted_sum'] += otherCentros * filtered_df['otroConsulta_100']
        filtered_df['weighted_sum'] += otherCentros * filtered_df['consultaPrimaria_100']
        filtered_df['weighted_sum'] += otherCentros * filtered_df['orgNoSanitaria_100']
        
        #Transport
        filtered_df['weighted_sum'] += distance * filtered_df['distanciaCentro_x']
        filtered_df['weighted_sum'] += vehicles * filtered_df['Bus_100']
        filtered_df['weighted_sum'] += vehicles * filtered_df['servicioCoches_100']
        filtered_df['weighted_sum'] += stations * filtered_df['estacionTren_100']
        filtered_df['weighted_sum'] += stations * filtered_df['estacionBus_100']
        
        #Work
        filtered_df['weighted_sum'] += trabajadoresZona * filtered_df['trabajadoresLugarTrabajo']
        filtered_df['weighted_sum'] += paro * filtered_df['paro_100']
        filtered_df['weighted_sum'] += trabajadoresZona * filtered_df['trabajadores_100']
        filtered_df['weighted_sum'] += trabajadoresZona * filtered_df['ocupadosColectivos_100']
        filtered_df['weighted_sum'] += pension * filtered_df['pensionistas_100']
        filtered_df['weighted_sum'] += highEduc * filtered_df['rentaBruta']
        filtered_df['weighted_sum'] += organizations * filtered_df['organizaciones_100']
        
        if sumImportances == 0:
            filtered_df['weighted_sum'] = (filtered_df.iloc[:, 1:22].sum(axis=1) + filtered_df.iloc[:, 23:60].sum(axis=1) + filtered_df.iloc[:, 61:62].sum(axis=1) + filtered_df.iloc[:, 63:67].sum(axis=1)) / 63
        else:
            filtered_df['weighted_sum'] = round(filtered_df['weighted_sum'] / sumImportances , 2)
        
        filtered_df['priceByArea_y'] = round(filtered_df['priceByArea_y'] , 2)
        try:
            filtered_df['Total_y'] = (filtered_df['Total_y']).astype(int)
            filtered_df['Total_y'] = filtered_df['Total_y'].map('{:,}'.format)
            filtered_df['Total_y'] = filtered_df['Total_y'].str.replace(',', '.')
        except:
            pass
        sorted_df = filtered_df.sort_values(by='weighted_sum', ascending=False)
        sorted_df = sorted_df.head(10)
        return render_template('final_results.html', data=sorted_df[['Municipio', 'weighted_sum','priceByArea_y','Total_y','distanciaCentro_y']])
    else:
         return render_template('economicDynamismMun.html')
   


if __name__ == '__main__':
    app.run(debug=True)
