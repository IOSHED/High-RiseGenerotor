import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import random


class Build:
    """Каркас для других классов"""

    max_height = 20
    min_height = 3
    box_grid = np.zeros([max_height, 5])
    night = True

    @classmethod
    def global_night(cls, night):
        if night:
            cls.night = True
        if not night:
            cls.night = False


class BuildResidentialBuilding(Build):
    """Класс жилого здания"""

    def __init__(self, height: int, width: int):
        super().__init__()
        self.windows = None
        self.grid_bild = None
        if BuildResidentialBuilding.check_height(height):
            self.height = height  # Высота
        self.width = width  # Ширина

    @classmethod
    def check_height(cls, arg):
        if cls.min_height <= arg <= cls.max_height:
            return True
        return False

    def math_front(self) -> np:
        """Математические действий для фасада"""

        grid_bild = np.ones((self.height, self.width))
        if not self.night:
            if random.randint(0, 1):
                for i in range(0, self.height):
                    for j in range(0, self.width):
                        grid_bild[i][j] = 3
            else:
                for i in range(0, self.height):
                    for j in range(0, self.width):
                        grid_bild[i][j] = 1
        self.grid_bild = self.math_grid(grid_bild, self.height, self.width, self.max_height)

    def math_windows(self) -> np:
        """Математические действия для окон жилого дома"""

        windows = np.zeros((self.height, self.width))
        for i in range(0, self.height):
            for j in range(0, self.width):
                if j % 2 != 0 and i % 2 != 0:
                    if self.night:
                        if random.randint(0, 1) == 0:
                            windows[i][j] = 3
                        else:
                            windows[i][j] = 1
                    if not self.night:
                        windows[i][j] = 2
        self.windows = self.math_grid(windows, self.height, self.width, self.max_height)
        self.grid_bild = self.grid_bild + self.windows

    def addendum(self) -> np:
        """Добавления к основнуму гриду грида здания"""
        self.box_grid = np.hstack([self.box_grid, self.grid_bild])
        return self.box_grid

    @staticmethod
    def math_grid(args, height: int, width: int, max_height) -> np:
        """Математические действия для возможности добавление гридов к основному"""

        args = np.append(args, [[0 for _ in range(0, width)]
                                for _ in range(0, max_height - height)], axis=0)
        args = np.append(args, [[0 for _ in range(0, height)]
                                for _ in range(0, max_height)], axis=1)
        args = np.flip(args)
        return args


class BuildingOffice(BuildResidentialBuilding):
    """Класс оффиса"""
    def __init__(self, height, width):
        super().__init__(height, width)
        self.grid_office = None

    def math_front_gradiente(self) -> np:
        """Создание градиента у фасада здания"""

        grid_office = np.ones([self.height, self.width])
        color_height = 2
        meaning_fill = 0.75
        while color_height < self.height and meaning_fill > 0:
            for i in range(color_height, self.height):
                grid_office[i] = meaning_fill
            color_height = color_height + 2
            meaning_fill = meaning_fill - 0.25

        self.grid_office = self.math_grid(grid_office, self.height, self.width, self.max_height)
        self.grid_bild = self.grid_bild + self.grid_office


class BuildingFabrik(BuildingOffice):
    """Класс фабрики"""
    def __init__(self, height, width):
        super().__init__(height, width)

    def math_windows(self) -> np:
        """Математические действия для уникальних окон"""

        windows = np.zeros((self.height, self.width))
        for i in range(0, self.height):
            for j in range(0, self.width):
                if j % 3 != 0 and i % 2 != 0:
                    if self.night:
                        windows[i][j] = 3
                    if not self.night:
                        windows[i][j] = 2
        self.windows = self.math_grid(windows, self.height, self.width, self.max_height)
        self.grid_bild = self.grid_bild + self.windows


class BildVoids(Build):
    """Создание пустоты в правом краю окна приложения"""

    @classmethod
    def bild_voids(cls) -> np:
        voids_grid = np.zeros([cls.max_height, 5])
        cls.box_grid = np.hstack([cls.box_grid, voids_grid])
        return cls.box_grid


class BildGrass(Build):
    """Создание травы и земли"""

    @classmethod
    def bild_grass(cls) -> np:
        grass = np.array([4 for _ in range(0, cls.box_grid.size // cls.max_height)])
        cls.box_grid = np.vstack([cls.box_grid, grass])
        return cls.box_grid


class PrintFront(Build):

    @classmethod
    def print_front(cls):
        if cls.night:
            sns.heatmap(cls.box_grid, annot=False, vmax=5, fmt="g", cbar=None, xticklabels=False,
                        yticklabels=False)
            plt.savefig("night_visualize_numpy_array.png", bbox_inches='tight', dpi=100)
            plt.title("Визуализация массива (ночь)", fontsize=12)
        if not cls.night:
            sns.heatmap(cls.box_grid, annot=False, vmax=5, center=2, cmap="plasma", fmt="g", cbar=None,
                        xticklabels=False, yticklabels=False)
            plt.savefig("day_visualize_numpy_array.png", bbox_inches='tight', dpi=100)
            plt.title("Визуализация массива (день)", fontsize=12)
        plt.show()
