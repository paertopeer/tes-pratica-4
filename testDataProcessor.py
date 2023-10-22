import os
import unittest
from dataProcessor import read_json_file

class TestDataProcessor(unittest.TestCase):
    current_directory = os.path.dirname(__file__)
    file_path = os.path.join(current_directory, "users.json")

    data = read_json_file(file_path)

    def test_read_json_file_success(self):
        self.assertEqual(len(self.data), 1000)  # Ajustar o número esperado de registros
        self.assertEqual(self.data[0]['name'], 'Robert James')
        self.assertEqual(self.data[1]['age'], 33)
        

    def test_read_json_file_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            read_json_file("non_existent.json")

    def test_read_json_file_invalid_json(self):
        with open("invalid.json", "w") as file:
            file.write("invalid json data")
        with self.assertRaises(ValueError):
            read_json_file("invalid.json")
            
    def ageInMonths(self, age):
        return age * 12
        
    def avgAgeCountry(self):
        ages_per_country = {}

        for item in self.data:
            ages = self.ageInMonths(item["age"])
            country = item["country"]
            
            if country in ages_per_country:
                ages_per_country[country].append(ages)
            else:
                ages_per_country[country] = [ages]
            
        avg_per_country = {}
        
        for country, ages in ages_per_country.items():
            avg =  sum(ages) // len(ages) 
            avg_per_country[country] = avg
        
        # return avg age per country
        return avg_per_country
    
    def olderCountry(self):
        older_per_country = {}

        for item in self.data:
            name = item['name']
            age = item["age"]
            country = item["country"]

            if country in older_per_country:
                if age > older_per_country[country][1]:
                    older_per_country[country] = (name, age)
            else:
                older_per_country[country] = (name, age)

        return older_per_country

    def peopleCount(self):
        count_people_per_country = {}

        for item in self.data:
            country = item["country"]

            if country in count_people_per_country:
                count_people_per_country[country] += 1
            else:
                count_people_per_country[country] = 1

        return count_people_per_country

    def test_avgAgeCountry(self):
        
        self.assertTrue(bool(self.data), "Arquivo JSON não está vazio")
        
        for person in self.data:
            # Valores de idade ausentes ou nulos
            self.assertIsNotNone(person['age'])
            #self.assertIn(person, person['age'])
            
            # Campo country ausente ou nulo
            self.assertIsNotNone(person['country'])
            #self.assertIn(person, person['age'])
            
        avg_per_country = self.avgAgeCountry()

        self.assertEqual(avg_per_country['UK'], 478)
    
    def test_olderCountry(self):
        self.assertEqual(self.olderCountry()['US'][1], 60)    
        self.assertEqual(self.olderCountry()['CA'][1], 59)    
        self.assertEqual(self.olderCountry()['JP'][1], 59)    
  

    def test_peopleCount(self):
         self.assertEqual(self.peopleCount()['US'], 133)  
         self.assertEqual(self.peopleCount()['UK'], 134)  
         self.assertEqual(self.peopleCount()['CA'], 103)  


if __name__ == '__main__':
    unittest.main()