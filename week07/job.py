# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod


class Animal(metaclass=ABCMeta):
    ANIMAL_SIZE_DICT = {
        "小": 2,
        "中": 5,
        "大": 8,
    }

    def __init__(self, animal_type, animal_size, animal_character):
        self.animal_type = animal_type
        self.animal_size = animal_size
        self.animal_character = animal_character
        self.is_fierce = self._is_fierce_animal(self.animal_type,
                                                self.animal_size,
                                                self.animal_character)

    def _is_fierce_animal(self, animal_type, animal_size, animal_character):
        if self.ANIMAL_SIZE_DICT[animal_size] >= 5 and \
                animal_type == '食肉' and \
                animal_character == '凶猛':
            return True
        return False

    @abstractmethod
    def show_animal_info(self):
        pass

    @abstractmethod
    def is_for_pet(self):
        pass

    @abstractmethod
    def get_species(self):
        pass


class Cat(Animal):
    SPECIES = 'CAT'

    def __init__(self, name, animal_type, animal_size, animal_character):
        super().__init__(animal_type, animal_size, animal_character)
        self.name = name
        self.fit_for_pet = self.is_for_pet()
        self._barking = '未知'

    def show_animal_info(self):
        print(f'Cat: {self.__dict__}')

    def is_for_pet(self):
        return False if self.is_fierce else True

    def get_species(self):
        return self.SPECIES

    @property
    def barking(self):
        return self._barking

    @barking.setter
    def barking(self, value):
        self._barking = value


class Dog(Cat):
    SPECIES = 'DOG'

    def show_animal_info(self):
        print(f'Dog: {self.__dict__}')

    def get_species(self):
        return self.SPECIES


class Zoo(object):

    def __init__(self, name):
        self.name = name
        self.animal_types = set()
        self.animals = set()

    def add_animal(self, instance):
        self.animal_types.add(instance.get_species())
        self.animals.add(instance)

    def add_animals(self, instance_list):
        for i in instance_list:
            self.add_animal(i)

    def __getattr__(self, item):
        try:
            if str(item).upper() in self.animal_types:
                return True
        except:
            return super(Zoo, self).__getattr__(item)
        return super(Zoo, self).__getattr__(item)


if __name__ == '__main__':
    # 实例化动物园
    z = Zoo('时间动物园')
    # 实例化，属性包括名字、类型、体型、性格
    animal_list = [
        Cat('大花猫 1', '食肉', '小', '温顺'),
        Cat('大花猫 2', '食草', '中', '凶猛'),
        Cat('大花猫 3', '食草', '大', '凶猛'),
        Dog('哈士奇 1', '食肉', '小', '凶猛'),
        Dog('哈士奇 2', '食草', '中', '温顺'),
        Cat('哈士奇 3', '食肉', '大', '凶猛'),
    ]
    animal_list[0].barking = '尖锐'
    animal_list[3].barking = '雄厚'

    z.add_animals(animal_list)
    print('Zoo:{}'.format(z.__dict__))
    # 动物园是否有这种动物
    have_cat = hasattr(z, 'Cat')
    have_dog = hasattr(z, 'Dog')
    have_elephant = hasattr(z, 'Elephant')
    print(f'Have cat? : {have_cat}\nHave dog? : {have_dog}\nHave elephant? : {have_elephant}')
