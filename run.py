import os 
import sys

def isAlreadyExist():
  if not os.path.exists("csv/provinces.csv"):
    return False
  if not os.path.exists("csv/regencies.csv"):
    return False
  if not os.path.exists("csv/districts.csv"):
    return False
  if not os.path.exists("csv/villages.csv"):
    return False
  return True

def main(argv):
  # If file exsists, continue
  if not isAlreadyExist() or "-f" in argv:
    # Run the script crawler.py
    print("Crawling data...")
    os.system("python script/crawler.py")
  else :
    print("Data already exists")
    print("If you want to update the data, please delete the data folder or -f option")
    
  # Run the script mdf_mysql_converter.py
  print("Converting to MySQL format...")
  os.system("python script/mdf_mysql_converter.py csv/provinces.csv csv/regencies.csv csv/districts.csv csv/villages.csv > sql/indonesia.sql")


if __name__ == "__main__":
  main(sys.argv[1:])