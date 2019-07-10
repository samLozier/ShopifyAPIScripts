# get dataframe with product information and on hand inventory. Currently really slow. 

import time
import requests
import pandas as pd


def get_all_upc():
    out = []  # the final output list of dictionaries to be converted to a DF
    continueprocess = True
    account = 'https://<APIkey:APIPASSWORD>@<Storename>'
    url_start = f"{account}.myshopify.com/admin/api/2019-07/products.json"
    next_link2 = ''
    outer_loopcount = 0
    while continueprocess is True:
        if outer_loopcount is 0:
            url_final = url_start
        else:
            url_final = next_link2
        response = requests.get(url_final)
        link_header = response.headers['Link'].split(',')
        if 'next' in response.headers['Link']:
            for link in link_header:
                if 'next' in link:
                    r = response.json()
                    next_link = link[link.find("<") + 1:link.find(">")].replace("https://<Storename>", f"{account}")
                    next_link2 = f"{next_link}"
                    outer_loopcount += 1
                    for product in r['products']:
                        time.sleep(1 / 2)
                        product_id = product['id']
                        url2 = f"{account}.myshopify.com/admin/api/2019-07/products/{product_id}/variants.json"
                        product_variant_request = requests.get(url2)
                        variant_response = product_variant_request.json()
                        for variant in variant_response['variants']:
                            newline = {'product_id': variant['product_id'], 'variant_id': variant['id'], 'upc': variant['barcode'],
                                       'quantity': variant['inventory_quantity']}
                            out.append(newline)
                        continueprocess = True
        else:
            for link in link_header:
                if 'previous' in link:
                    r = response.json()
                    next_link = link[link.find("<") + 1:link.find(">")].replace("https://<storename>", f"{account}")
                    next_link2 = f"{next_link}"
                    outer_loopcount += 1

                    for product in r['products']:
                        time.sleep(1 / 2)
                        product_id = product['id']
                        url2 = f"{account}.myshopify.com/admin/api/2019-07/products/{product_id}/variants.json"
                        product_variant_request = requests.get(url2)
                        variant_response = product_variant_request.json()
                        for variant in variant_response['variants']:
                            newline = {'product_id': variant['product_id'], 'variant_id': variant['id'],
                                       'upc': variant['barcode'],
                                       'quantity': variant['inventory_quantity']}
                            out.append(newline)
                continueprocess = False

    df = pd.DataFrame(out)
    return df


df_barcodes = get_all_upc()
