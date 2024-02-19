import logging
import os
import traceback
from datetime import datetime

import pandas as pd

from flipkart_scrapper import scrape_product_data

logging.basicConfig(filename='scraping.log', level=logging.DEBUG)

# retry = [
#     'MOBGHWFHECFVMDCX',
#     'MOBGTAGPTB3VS24W',
#     'BOTGS2VEVUWTZDXJ',
#     'BOTGKQKPYZAUCAK9',
#     'BOTF7Q4VTVNEZQWZ',
#     'BOTGJF9XR47BPFPY',
#     'BOTFN2MFQADDD8VR',
#     'BOTGG9VGBFZ58HJN',
#     'BOTGS2VEZAYXAFD8',
#     'BOTGS2XBN9XTR33Q',
#     'BOTGS2WRSTKTGWE3',
#     'BOTFMYYRRHW5X3AD',
#     'BOTFTZKNVGYSYHZJ',
#     'BOTGXE3ZGAD3XJU5',
# ]


def lambda_handler():
    try:
        # Read FSNs from CSV file
        products_df = pd.read_csv('BOROSIL.csv')
        products_tuple = tuple(products_df['FSN'])
        all_data = []

        for i, fsn in enumerate(products_tuple, start=1):
            print(f'Scraping Product {i}: {fsn}')
            try:
                product_data = scrape_product_data(fsn)
                if product_data:
                    all_data.append(product_data)
            except Exception as e:
                logging.error(f"Error scraping product {i}: {e} : {fsn}")
                return {
                    "statusCode": 500,
                    "body": {
                        "error": f"Error scraping product {i}: {e}"
                    }
                }

        logging.info("Data scraping completed successfully.")
        excel_file_path = export_to_excel(all_data)
        logging.info(f"Data exported to '{excel_file_path}' successfully.")
        print(f"Excel file exported to: {excel_file_path}")

        return {
            "statusCode": 200,
            "body": {
                "all_data": all_data,
                "excel_file_path": excel_file_path
            }
        }
    except Exception as e:
        logging.error(f"Unhandled error: {e}")
        traceback.print_exc()
        return {
            "statusCode": 500,
            "body": {
                "error": str(e)
            }
        }


def export_to_excel(data):
    df = pd.DataFrame(data)
    directory = 'C:/Users/Admin/Downloads'
    os.makedirs(directory, exist_ok=True)
    current_datetime = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    excel_file_name = f'flipkart_data_{current_datetime}.xlsx'
    excel_file_path = os.path.join(directory, excel_file_name)
    with pd.ExcelWriter(excel_file_path, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False)
    return excel_file_path


lambda_handler()
