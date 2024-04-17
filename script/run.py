# Indonesia Administrative Area Code

import os
import sys
import json
import requests

all_province_url = "http://sirekap-obj-data.kpu.go.id/wilayah/pemilu/ppwp/0.json"

# remove warning
requests.packages.urllib3.disable_warnings()

def clear_file():
    with open("data/provinces.csv", "w") as f:
        f.write("")

    with open("data/regencies.csv", "w") as f:
        f.write("")
    
    with open("data/districts.csv", "w") as f:
        f.write("")
    
    with open("data/villages.csv", "w") as f:
        f.write("")

def get_district(province_code, regency_code):
    district_url = f"http://sirekap-obj-data.kpu.go.id/wilayah/pemilu/ppwp/{province_code}/{regency_code}.json"
    response = requests.get(district_url, verify=False)
    data = response.json()

    # Mapping district code to district name
    # province_code, regency_code, district_code, district_name
    district_code = []
    for district in data:
        district_code.append(( district["kode"], regency_code, district["nama"]))
    
    # Sort by province code, regency code, and district code
    district_code = sorted(district_code, key=lambda x: (x[0], x[1]))
    return district_code

def get_regencies(province_code):
    
    regency_url = f"http://sirekap-obj-data.kpu.go.id/wilayah/pemilu/ppwp/{province_code}.json"
    response = requests.get(regency_url, verify=False)
    data = response.json()

    # Mapping regency code to regency name
    # province_code, regency_code, regency_name
    regency_code = []
    for regency in data:
        regency_code.append(( regency["kode"], province_code, regency["nama"]))

    # Sort by province code, and secondly by regency code 
    regency_code = sorted(regency_code, key=lambda x: (x[0], x[1]))

    return regency_code

def get_villages(province_code, regency_code, district_code):
    village_url = f"http://sirekap-obj-data.kpu.go.id/wilayah/pemilu/ppwp/{province_code}/{regency_code}/{district_code}.json"
    response = requests.get(village_url, verify=False)
    data = response.json()

    # Mapping village code to village name
    # province_code, regency_code, district_code, village_code, village_name
    village_code = []
    for village in data:
        village_code.append(( village["kode"], district_code, village["nama"])) 
    
    # Sort by province code, regency code, district code, and village code
    village_code = sorted(village_code, key=lambda x: (x[0], x[1]))
    return village_code

def main():
    #  Clear file
    clear_file()

    response = requests.get(all_province_url, verify=False)
    data = response.json()

    # Mapping province code to province name
    province_code = {}

    for province in data:
        if (province["kode"] == "99"):
            continue
        province_code[province["kode"]] = province["nama"]

        # If detect white space in first character, remove it
        if province_code[province["kode"]][0] == " ":
            province_code[province["kode"]] = province_code[province["kode"]][1:]

    # Sort by province code
    province_code = dict(sorted(province_code.items()))

    # # Write to file
    with open("data/provinces.csv", "a") as f:
        for code, name in province_code.items():
            f.write(f"{code},{name}\n")

    # Get regencies
    with open("data/regencies.csv", "a") as f:
        for code in province_code.keys():
            
            # Await for prevent rate limit
            regency_code = get_regencies(code)
            for regency in regency_code:
                f.write(f"{regency[0]},{regency[1]},{regency[2]}\n")
            

    # Get districts
    with open("data/districts.csv", "a") as f:
        # Read from regencies.csv
        with open("data/regencies.csv", "r") as regency_file:
            regency_code = regency_file.readlines()
            
            for regency in regency_code:           
                regency_code, province_code, _ = regency.split(",")
                district_code = get_district(province_code, regency_code)
                for district in district_code:
                    f.write(f"{district[0]},{district[1]},{district[2]}\n")
        # Close
        regency_file.close()

    # Get villages
    with open("data/villages.csv", "a") as f:
        # Read from districts.csv
        with open("data/districts.csv", "r") as district_file:
            district_code = district_file.readlines()
            for district in district_code:
                district_code, regency_code, _ = district.split(",")
                
                # Province code is 2 first character of regency code
                province_code = regency_code[:2]
                village_code = get_villages(province_code, regency_code, district_code)

                for village in village_code:
                    f.write(f"{village[0]},{village[1]},{village[2]}\n")
        # Close
        district_file.close()

if __name__ == "__main__":
    main()