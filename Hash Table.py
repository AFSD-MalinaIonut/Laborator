import csv
import random
import os
import hashlib
from datetime import datetime
from collections import defaultdict


JUDETE_DISTRIBUTION = {
    1: 0.066,
    2: 0.047,

    41: 0.061  
}

GENDER_DISTRIBUTION = {'M': 0.48, 'F': 0.52}

AGE_DISTRIBUTION = {
    '1950-1960': 0.08,
    '1961-1970': 0.12,
    '1971-1980': 0.15,
    '1981-1990': 0.18,
    '1991-2000': 0.22,
    '2001-2010': 0.25
}


class CNPGenerator:
    @staticmethod
    def calculate_control_digit(cnp_12):

        weights = [2, 7, 9, 1, 4, 6, 3, 5, 8, 2, 7, 9]
        total = sum(int(c) * w for c, w in zip(cnp_12, weights))
        return 1 if total % 11 == 10 else total % 11

    @staticmethod
    def generate_cnp(sex, birth_year, county, sequential_number):

        s = '1' if sex == 'M' else '2'
        aa = str(birth_year % 100).zfill(2)
        ll = str(random.randint(1, 12)).zfill(2)
        zz = str(random.randint(1, 28)).zfill(2)
        jj = str(county).zfill(2)
        nnn = str(sequential_number).zfill(3)

        cnp_12 = s + aa + ll + zz + jj + nnn
        c = str(CNPGenerator.calculate_control_digit(cnp_12))
        return cnp_12 + c


class DataGenerator:
    @staticmethod
    def generate_names(count):

        from faker import Faker
        fake = Faker('ro_RO')
        names = []
        for _ in range(count):
            gender = random.choices(['M', 'F'], weights=[0.48, 0.52])[0]
            if gender == 'M':
                names.append(f"{fake.first_name_male()} {fake.last_name()}")
            else:
                names.append(f"{fake.first_name_female()} {fake.last_name()}")
        return names

    @staticmethod
    def generate_csv(filename='cnp_data.csv', count=1_000_000):


        birth_years = []
        for _ in range(count):
            age_group = random.choices(
                list(AGE_DISTRIBUTION.keys()),
                weights=list(AGE_DISTRIBUTION.values())
            )[0]
            start, end = map(int, age_group.split('-'))
            birth_years.append(random.randint(start, end))


        counties = random.choices(
            list(JUDETE_DISTRIBUTION.keys()),
            weights=list(JUDETE_DISTRIBUTION.values()),
            k=count
        )


        genders = random.choices(
            list(GENDER_DISTRIBUTION.keys()),
            weights=list(GENDER_DISTRIBUTION.values()),
            k=count
        )


        names = DataGenerator.generate_names(count)


        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            for i in range(count):
                cnp = CNPGenerator.generate_cnp(
                    genders[i],
                    birth_years[i],
                    counties[i],
                    i % 999 + 1
                )
                writer.writerow([cnp, names[i]])

        print(f"Generated {count} CNPs in {filename}")


class HashTable:
    def __init__(self, size=1_000_003):
        self.size = size
        self.table = [None] * size
        self.count = 0
        self.collisions = 0

    def hash_function(self, key):

        p = 31
        m = self.size
        hash_value = 0
        p_pow = 1
        for c in key:
            hash_value = (hash_value + ord(c) * p_pow) % m
            p_pow = (p_pow * p) % m
        return hash_value

    def insert(self, key, value):

        if self.count / self.size > 0.7:
            self._resize()

        index = self.hash_function(key)
        original_index = index
        probes = 0

        while True:
            if self.table[index] is None:
                self.table[index] = (key, value)
                self.count += 1
                return probes
            elif self.table[index][0] == key:
                self.table[index] = (key, value)
                return probes
            else:
                self.collisions += 1
                probes += 1
                index = (original_index + probes) % self.size

    def _resize(self):

        old_table = self.table
        self.size = self.size * 2 + 1
        self.table = [None] * self.size
        self.count = 0
        self.collisions = 0

        for item in old_table:
            if item is not None:
                self.insert(item[0], item[1])

    def search(self, key):

        index = self.hash_function(key)
        original_index = index
        probes = 0

        while True:
            if self.table[index] is None:
                return None, probes
            elif self.table[index][0] == key:
                return self.table[index][1], probes
            else:
                probes += 1
                index = (original_index + probes) % self.size
                if probes > self.size:
                    return None, probes


class PerformanceAnalyzer:
    @staticmethod
    def analyze(hash_table, sample_size=1000, filename='cnp_data.csv'):


        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            cnps = [row[0] for row in reader]


        sample = random.sample(cnps, min(sample_size, len(cnps)))

        total_probes = 0
        found = 0
        not_found = 0
        max_probes = 0

        for cnp in sample:
            result, probes = hash_table.search(cnp)
            total_probes += probes
            max_probes = max(max_probes, probes)
            if result is not None:
                found += 1
            else:
                not_found += 1

        print("\n=== Performance Analysis ===")
        print(f"Total searches: {sample_size}")
        print(f"Found: {found} | Not found: {not_found}")
        print(f"Total probes: {total_probes}")
        print(f"Average probes per search: {total_probes / sample_size:.2f}")
        print(f"Maximum probes in a search: {max_probes}")
        print(f"Collisions during insertion: {hash_table.collisions}")
        print(f"Load factor: {hash_table.count / hash_table.size:.2f}")


def main():
    print("=== CNP Hash Table Project ===")


    print("\n[Stage 1] Generating CNP data...")
    if not os.path.exists('cnp_data.csv'):
        DataGenerator.generate_csv('cnp_data.csv', 1_000_000)
    else:
        print("CNP data file already exists. Using existing file.")


    print("\n[Stage 2] Creating and populating hash table...")
    hash_table = HashTable()

    with open('cnp_data.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            if i >= 1_000_000:
                break
            hash_table.insert(row[0], row[1])
            if i % 100_000 == 0:
                print(f"Inserted {i:,} records...")

    print(f"Hash table populated with {hash_table.count:,} records.")


    print("\n[Stage 3] Analyzing performance...")
    PerformanceAnalyzer.analyze(hash_table)





if __name__ == '__main__':
    main()