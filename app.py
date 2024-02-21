from flask import Flask, render_template, request, redirect
import pandas as pd
import copy

app = Flask(__name__)

df = pd.read_csv('./clustersAtractivoJuntos_variablesWeb.csv') 
df_extra = pd.read_csv('./distritosAtractivoJuntos_variablesWeb.csv') 

@app.route('/')
def index():
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
        return render_template('select_importance.html', groups=groups)
    
@app.route('/madrid')
def madrid():
    return render_template('select_importance_extra.html')

@app.route('/final_results_extra', methods=['POST'])
def final_results_extra():
    importances = [int(request.form['private_education']),int(request.form['public_education']),int(request.form['libraries']),
    int(request.form['foreigner_student']),int(request.form['special_student']),
    int(request.form['accidentes']),int(request.form['detenidos']),int(request.form['policia']),
    int(request.form['total_population']), int(request.form['density']), int(request.form['women']),
    int(request.form['foreigners']), int(request.form['young']), int(request.form['highEduc']),
    int(request.form['sport_greenareas']), int(request.form['espectaculos']), int(request.form['residuos']),
    int(request.form['vulnerabilidad']), int(request.form['añoConstruccion']), int(request.form['good_houses']),
    int(request.form['houses']), int(request.form['size']), int(request.form['general_features']),
    int(request.form['new_development']), int(request.form['price']), int(request.form['chalets']),
    int(request.form['centros']), int(request.form['mayores']), int(request.form['otherCentros']),
    int(request.form['bicis']), int(request.form['metro']), int(request.form['paro']),
    int(request.form['pension']), int(request.form['renta']), int(request.form['locales'])]
    
    #Se coge la suma de importances para normalizar la atractividad final
    sumImportances = sum(importances)
    sumImportances += importances[0] #se añade el numero de veces que se utiliza cada importancia
    sumImportances += importances[1]
    sumImportances += 4 * importances[14]
    sumImportances += importances[15]
    sumImportances += importances[24]
    sumImportances += 2 * importances[21]
    sumImportances += 2 * importances[22]
    sumImportances += importances[19]
    sumImportances += importances[26]
    sumImportances += 3 * importances[27]
    sumImportances += 2 * importances[28]
    sumImportances += importances[29]
    sumImportances += importances[33]
    
    df_extra['weighted_sum'] = 0
    
    #Education
    df_extra['weighted_sum'] += importances[0] * df_extra['centrosPrivadoporAlumno_100']
    df_extra['weighted_sum'] += importances[0] * df_extra['centrosPrivadoporAlumnoExtr_100']
    df_extra['weighted_sum'] += importances[1] * df_extra['centrosPublicoporAlumno_100']
    df_extra['weighted_sum'] += importances[1] * df_extra['centrosPublicoporAlumnoExtr_100']
    df_extra['weighted_sum'] += importances[2] * df_extra['bibliotecas_100']
    df_extra['weighted_sum'] += importances[3] * df_extra['porcAlumnoExtranjero']
    df_extra['weighted_sum'] += importances[4] * df_extra['porcApoyoEducativo']
    
    #Security
    df_extra['weighted_sum'] += importances[5] * df_extra['Atestados/partes de accidentes de tráfico confeccionados']
    df_extra['weighted_sum'] += importances[6] * df_extra['detenidos_100']
    df_extra['weighted_sum'] += importances[7] * df_extra['sumaIntervecniones']
    
    #Population and general
    df_extra['weighted_sum'] += importances[8] * df_extra['Número Habitantes_x']
    df_extra['weighted_sum'] += importances[9] * df_extra['Población densidad (hab./Ha.)']
    df_extra['weighted_sum'] += importances[10] * df_extra['frac_mujeres']
    df_extra['weighted_sum'] += importances[11] * df_extra['frac_extranjeros']
    df_extra['weighted_sum'] += importances[12] * df_extra['frac_young']
    df_extra['weighted_sum'] += importances[13] * df_extra['frac_HighEduc']
    df_extra['weighted_sum'] += importances[14] * df_extra['zonasVerdes(ha)']
    df_extra['weighted_sum'] += importances[14] * df_extra['superficieDeportiva(m2)']
    df_extra['weighted_sum'] += importances[14] * df_extra['centrosDeportivos_100']
    df_extra['weighted_sum'] += importances[14] * df_extra['instalacionesDeportivasBasicas_100']
    df_extra['weighted_sum'] += importances[14] * df_extra['piscinasCubiertas_100']
    df_extra['weighted_sum'] += importances[15] * df_extra['espaciosCulturales_100']
    df_extra['weighted_sum'] += importances[15] * df_extra['espectaculos_100']
    df_extra['weighted_sum'] += importances[16] * df_extra['residuos(kg/hab/dia)']
    df_extra['weighted_sum'] += importances[17] * df_extra['posicionVulnerabilidad_x']
    
    #Housing
    df_extra['weighted_sum'] += importances[18] * df_extra['añoMedioConstruccion']
    df_extra['weighted_sum'] += importances[19] * df_extra['Viviendas en estado bueno']
    df_extra['weighted_sum'] += importances[19] * df_extra['viviendasMalEstado']
    df_extra['weighted_sum'] += importances[20] * df_extra['viviendas_habitante']
    df_extra['weighted_sum'] += importances[21] * df_extra['size']
    df_extra['weighted_sum'] += importances[21] * df_extra['rooms']
    df_extra['weighted_sum'] += importances[21] * df_extra['bathrooms']
    df_extra['weighted_sum'] += importances[22] * df_extra['hasLift']
    df_extra['weighted_sum'] += importances[22] * df_extra['parkingSpace']
    df_extra['weighted_sum'] += importances[22] * df_extra['pisoBajo']
    df_extra['weighted_sum'] += importances[23] * df_extra['newDevelopment']
    df_extra['weighted_sum'] += importances[25] * df_extra['propertyType']
    df_extra['weighted_sum'] += importances[24] * df_extra['priceByArea_x']
    df_extra['weighted_sum'] += importances[24] * df_extra['price']
    
    #Sanity
    df_extra['weighted_sum'] += importances[26] * df_extra['CentrosSalud_100']
    df_extra['weighted_sum'] += importances[26] * df_extra['HospitalesClinicasSanatorios_100']
    df_extra['weighted_sum'] += importances[27] * df_extra['CentrosMayores_100']
    df_extra['weighted_sum'] += importances[27] * df_extra['ServiciosSociales_100']
    df_extra['weighted_sum'] += importances[27] * df_extra['AuxHogar_100']
    df_extra['weighted_sum'] += importances[27] * df_extra['socioCentrosMayores_100']
    df_extra['weighted_sum'] += importances[28] * df_extra['drogas/especialidades_100']
    df_extra['weighted_sum'] += importances[28] * df_extra['CentrosSaludMental_100']
    df_extra['weighted_sum'] += importances[28] * df_extra['CentrosAlzheimer_100']
    
    #Transport
    df_extra['weighted_sum'] += importances[29] * df_extra['estBici_100']
    df_extra['weighted_sum'] += importances[29] * df_extra['numBici_100']
    df_extra['weighted_sum'] += importances[30] * df_extra['metro_100']
    
    #Work
    df_extra['weighted_sum'] += importances[31] * df_extra['paro_100']
    df_extra['weighted_sum'] += importances[32] * df_extra['pensionMedia']
    df_extra['weighted_sum'] += importances[33] * df_extra['crecimientoRentaPC']
    df_extra['weighted_sum'] += importances[33] * df_extra['rentaMedia']
    df_extra['weighted_sum'] += importances[34] * df_extra['localesAbiertos_100']
    
    
    df_extra['weighted_sum'] = round(df_extra['weighted_sum'] / sumImportances , 2)
    sorted_df = df_extra.sort_values(by='weighted_sum', ascending=False)
    return render_template('final_results_extra.html', data=sorted_df[['distrito', 'weighted_sum','priceByArea_y','Número Habitantes_y','posicionVulnerabilidad_y']])

@app.route('/final_results', methods=['POST'])
def final_results():
    importances = [int(request.form['private_education']),int(request.form['public_education']),
    int(request.form['libraries']),int(request.form['activities_education']),
    int(request.form['air_quality']), int(request.form['temperature']),
    int(request.form['solar_radiation']), int(request.form['rain']),
    int(request.form['total_population']), int(request.form['density']),
    int(request.form['average_age']),int(request.form['foreigners']),
    int(request.form['young']),  int(request.form['highEduc']),
    int(request.form['servicios_generales']), int(request.form['familiar_houses']),
    int(request.form['urban_units']), int(request.form['oneToThree']),
    int(request.form['fourMore']), int(request.form['size']),
    int(request.form['general_features']), int(request.form['new_development']),
    int(request.form['price']), int(request.form['chalets']),
    int(request.form['centros']), int(request.form['pharmacy']),
    int(request.form['otherCentros']), int(request.form['distance']),
    int(request.form['vehicles']), int(request.form['stations']),
    int(request.form['trabajadoresZona']), int(request.form['paro']),
    int(request.form['workRatio']), int(request.form['pension']),
    int(request.form['renta']), int(request.form['organizations']),
    int(request.form['funcionarios'])]  
    
    #Se coge la suma de importances para normalizar la atractividad final
    sumImportances = sum(importances)
    sumImportances += 2 * importances[0] #se añade el numero de veces que se utiliza cada importancia
    sumImportances += 2 * importances[1]
    sumImportances += importances[3]
    sumImportances += 5 * importances[4]
    sumImportances += importances[14]
    sumImportances += 2 * importances[15]
    sumImportances += importances[16]
    sumImportances += 2 * importances[19]
    sumImportances += 2 * importances[20]
    sumImportances += importances[22]
    sumImportances += 4 * importances[26]
    sumImportances += importances[28]
    sumImportances += importances[29]
    sumImportances += importances[32]
    
    filtered_df['weighted_sum'] = 0
    
    #Education
    filtered_df['weighted_sum'] += importances[0] * filtered_df['escuelas/100_alumnos_priv']
    filtered_df['weighted_sum'] += importances[0] * filtered_df['unidadEsc/100_alumnos_priv']
    filtered_df['weighted_sum'] += importances[0] * filtered_df['profesores/100_alumnos_priv']
    filtered_df['weighted_sum'] += importances[1] * filtered_df['escuelas/100_alumnos_pub']
    filtered_df['weighted_sum'] += importances[1] * filtered_df['unidadEsc/100_alumnos_pub']
    filtered_df['weighted_sum'] += importances[1] * filtered_df['profesores/100_alumnos_pub']
    filtered_df['weighted_sum'] += importances[2] * filtered_df['bibliotecas/100_alumnos']
    filtered_df['weighted_sum'] += importances[3] * filtered_df['idiomas/10_alumnos']
    filtered_df['weighted_sum'] += importances[3] * filtered_df['actividades/10_alumnos']
    
    #Air quality
    filtered_df['weighted_sum'] += importances[4] * filtered_df['Magnitud6']
    filtered_df['weighted_sum'] += importances[4] * filtered_df['Magnitud7']
    filtered_df['weighted_sum'] += importances[4] * filtered_df['Magnitud8']
    filtered_df['weighted_sum'] += importances[4] * filtered_df['Magnitud10']
    filtered_df['weighted_sum'] += importances[4] * filtered_df['Magnitud12']
    filtered_df['weighted_sum'] += importances[4] * filtered_df['Magnitud14']
    filtered_df['weighted_sum'] += importances[5] * filtered_df['Magnitud83']
    filtered_df['weighted_sum'] += importances[6] * filtered_df['Magnitud88']
    filtered_df['weighted_sum'] += importances[7] * filtered_df['Magnitud89']
    
    #Population and general
    filtered_df['weighted_sum'] += importances[8] * filtered_df['Total_x']
    filtered_df['weighted_sum'] += importances[9] * filtered_df['densidad']
    filtered_df['weighted_sum'] += importances[10] * filtered_df['edadMedia']
    filtered_df['weighted_sum'] += importances[11] * filtered_df['frac_extranjeros']
    filtered_df['weighted_sum'] += importances[12] * filtered_df['frac_young']
    filtered_df['weighted_sum'] += importances[13] * filtered_df['frac_HighEduc']
    filtered_df['weighted_sum'] += importances[14] * filtered_df['serviciosOcio']
    filtered_df['weighted_sum'] += importances[14] * filtered_df['serviciosGenerales']
    
    #Housing
    filtered_df['weighted_sum'] += importances[15] * filtered_df['familiares']
    filtered_df['weighted_sum'] += importances[15] * filtered_df['antiguedadFamiliares']
    filtered_df['weighted_sum'] += importances[15] * filtered_df['superficieFamiliares']
    filtered_df['weighted_sum'] += importances[16] * filtered_df['unidadesUrbanasResidenciales']
    filtered_df['weighted_sum'] += importances[16] * filtered_df['numHouses']
    filtered_df['weighted_sum'] += importances[17] * filtered_df['1-3p']
    filtered_df['weighted_sum'] += importances[18] * filtered_df['4+p']
    filtered_df['weighted_sum'] += importances[19] * filtered_df['size']
    filtered_df['weighted_sum'] += importances[19] * filtered_df['rooms']
    filtered_df['weighted_sum'] += importances[19] * filtered_df['bathrooms']
    filtered_df['weighted_sum'] += importances[20] * filtered_df['hasLift']
    filtered_df['weighted_sum'] += importances[20] * filtered_df['parkingSpace']
    filtered_df['weighted_sum'] += importances[20] * filtered_df['pisoBajo']
    filtered_df['weighted_sum'] += importances[21] * filtered_df['newDevelopment']
    filtered_df['weighted_sum'] += importances[23] * filtered_df['propertyType']
    filtered_df['weighted_sum'] += importances[22] * filtered_df['priceByArea_x']
    filtered_df['weighted_sum'] += importances[22] * filtered_df['price']
    
    #Sanity
    filtered_df['weighted_sum'] += importances[24] * filtered_df['centros_100']
    filtered_df['weighted_sum'] += importances[25] * filtered_df['farmacias_100']
    filtered_df['weighted_sum'] += importances[26] * filtered_df['centrosSociales_10']
    filtered_df['weighted_sum'] += importances[26] * filtered_df['clinicaDental_10']
    filtered_df['weighted_sum'] += importances[26] * filtered_df['otroConsulta_100']
    filtered_df['weighted_sum'] += importances[26] * filtered_df['consultaPrimaria_100']
    filtered_df['weighted_sum'] += importances[26] * filtered_df['orgNoSanitaria_100']
    
    #Transport
    filtered_df['weighted_sum'] += importances[27] * filtered_df['distanciaCentro_x']
    filtered_df['weighted_sum'] += importances[28] * filtered_df['Bus_100']
    filtered_df['weighted_sum'] += importances[28] * filtered_df['servicioCoches_100']
    filtered_df['weighted_sum'] += importances[29] * filtered_df['estacionTren_100']
    filtered_df['weighted_sum'] += importances[29] * filtered_df['estacionBus_100']
    
    #Work
    filtered_df['weighted_sum'] += importances[30] * filtered_df['trabajadoresLugarTrabajo']
    filtered_df['weighted_sum'] += importances[31] * filtered_df['paro_100']
    filtered_df['weighted_sum'] += importances[32] * filtered_df['trabajadores_100']
    filtered_df['weighted_sum'] += importances[32] * filtered_df['ocupadosColectivos_100']
    filtered_df['weighted_sum'] += importances[33] * filtered_df['pensionistas_100']
    filtered_df['weighted_sum'] += importances[34] * filtered_df['rentaBruta']
    filtered_df['weighted_sum'] += importances[35] * filtered_df['organizaciones_100']
    filtered_df['weighted_sum'] += importances[36] * filtered_df['funcionario_100']
    
    
    filtered_df['weighted_sum'] = round(filtered_df['weighted_sum'] / sumImportances , 2)
    sorted_df = filtered_df.sort_values(by='weighted_sum', ascending=False)
    return render_template('final_results.html', data=sorted_df[['Municipio', 'weighted_sum','priceByArea_y','Total_y','distanciaCentro_y']])

if __name__ == '__main__':
    app.run(debug=True)
