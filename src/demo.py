from random import shuffle, seed
from faker.providers.person.uk_UA import Provider

first_names = list(set(Provider.first_names))

seed(4321)
shuffle(first_names)

print(first_names[0:1000])