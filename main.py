from bs4 import BeautifulSoup
import requests
import pandas as pd


# number_of_pages = int(input("Escolhe o numero de paginas: "))
# url = input("Escolhe o URL (nao fazer copy-paste de '/pagina-<i>)': ")
# file_name = input("Escolhe o nome do ficheiro: ")


def get_houses(number_of_pages, url, file_name):
    houses = []

    for i in range(1, number_of_pages):
        r = requests.get(url + f'/pagina-{i}').text
        soup_one = BeautifulSoup(r, 'html.parser')

        list_property = soup_one.find('div', class_='list-properties')
        for properties in list_property.find_all('div',
                                                 class_=['property big-picture', 'property featured big-picture',
                                                         'property']):
            property_list_title = properties.find('a').get('href').replace('-', ' ').replace('/', ' ').replace('venda ',
                                                                                                               "")
            property_price = float(
                properties.find('div', class_='property-price').find('span').get_text().strip().replace(" €",
                                                                                                        "").replace('.',
                                                                                                                    ''))
            property_price_change = properties.find('div', class_='property-price').find('span',
                                                                                         class_='property-price-change-value')
            if property_price_change is None:
                property_price_change = 'NA'
            else:
                property_price_change = float(properties.find('div', class_='property-price').find('span',
                                                                                                   class_='property-price-change-value').get_text().strip().replace(
                    " €", "").replace('.', ''))

            number_of_bedrooms = 0
            area = 0
            area_terrain = 0
            energy_certificate = "NA"

            property_features = (properties.find('div', class_='property-features').find_all('span'))
            for item in property_features:
                try:
                    feature_text = item.get_text()
                    if 'quartos' in feature_text:
                        number_of_bedrooms = int(feature_text.replace(' quartos', ''))
                    elif 'm²' in feature_text and 'Terreno' not in feature_text:
                        area = float(feature_text.replace(' m²', ''))
                    elif 'm²' in feature_text and 'Terreno' in feature_text:
                        area_terrain = float(feature_text.replace('Terreno ', '').replace(' m²', ''))
                    elif 'C.E.' in feature_text:
                        energy_certificate = feature_text.replace('C.E.: ', '')
                except:
                    pass

            # check if each property feature has been assigned a value
            number_of_bedrooms = number_of_bedrooms if 'number_of_bedrooms' in locals() else 'N.A.'
            area = area if 'area' in locals() else 'N.A.'
            area_terrain = area_terrain if 'area_terrain' in locals() else 'N.A.'
            energy_certificate = energy_certificate if 'energy_certificate' in locals() else 'N.A.'

            property_description = properties.find('div', class_='property-description-text').get_text()
            property_link = 'https://supercasa.pt' + str(properties.find('a').get('href'))
            house_id = property_link.split('/')[-1]

            e = requests.get(property_link).text

            soup_two = BeautifulSoup(e, 'html.parser')
            detail_info = soup_two.find('div', class_='detail-info')
            location_detail = detail_info.find('div', class_='property-list-title').get_text().split(',')
            year_of_construction = detail_info.find('div', class_='property-features').find_all('span')
            if len(year_of_construction) == 2:
                year_of_construction = (year_of_construction[1]).get_text().replace("Ano construção: ", "")
            else:
                year_of_construction = 'NA'
            location_district = location_detail[-1].replace(' ', '').replace(' Vermapa', '')
            location_council = location_detail[-2].replace(' ', '')
            if len(location_detail) == 3:
                location_zone = location_detail[0]
            else:
                location_zone = 'NA'

            detail_floorplan_icon = detail_info.find('div', class_='detail-media-menu')
            if detail_floorplan_icon is not None:
                try:
                    blueprint_span = detail_floorplan_icon.select_one(".detail-floorplan-icon + span")
                    blueprint = blueprint_span.text.strip()
                except AttributeError:
                    blueprint = 'NA'

            lift = 'NAO'
            balcony = 'NAO'
            garage = 'NAO'

            detail_info_features_list = detail_info.find('div', class_='detail-info-features-list')
            for item in detail_info_features_list.find_all('ul'):

                for items in item.find_all('li'):
                    if 'Elevador' in items.get_text():
                        lift = "SIM"
                    if 'Varandas' in items.get_text():
                        balcony = "SIM"
                    if 'Garagem' in items.get_text():
                        garage = 'SIM'

            house_dict = {'page': i, 'house_id': house_id, 'link': property_link, 'titulo': property_list_title,
                          'planta': blueprint,
                          'ano de construcao': year_of_construction,
                          'distrito': location_district,
                          'concelho': location_council, 'zona': location_zone,
                          'preco depois': property_price, 'preco antes': property_price_change, 'elevador': lift,
                          'varanda': balcony, 'garagem': garage,
                          'quartos': number_of_bedrooms, 'area': area,
                          'area terreno': area_terrain,
                          'CE': energy_certificate, 'descricao': property_description}
            houses.append(house_dict)
            print(f'Mais uma pagina adicionada, ainda vamos na pagina {i}!')

    df = pd.DataFrame(houses)
    file = df.to_csv(f'{file_name}.csv')
    print(file)

    return 'Finish!'

# print(get_houses())
