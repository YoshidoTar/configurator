class ConfigLogic:
    PROCESSORS = {
        "Intel Core i5-12400f": {
            "brand": "Intel",
            "socket": "LGA1700",
            "tpd": 65,
            "min_psu": 450,
            "motherboards": ["GIGABYTE H610M", "ASUS PRIME B560M", "MSI PRO B660M-A"],
            "description": "Отличный выбор для бюджетных игровых сборок. Хорошая производительность за свои деньги."
        },
        "Intel Core i5-13600": {
            "brand": "Intel",
            "socket": "LGA1700",
            "tpd": 65,
            "min_psu": 500,
            "motherboards": ["GIGABYTE B660M", "ASUS PRIME Z690-P", "MSI PRO Z690-A"],
            "description": "Современный процессор для игр и работы. Поддержка DDR5."
        },
        "Intel Core i3-12100": {
            "brand": "Intel",
            "socket": "LGA1700",
            "tpd": 60,
            "min_psu": 400,
            "motherboards": ["ASUS PRIME H610M-A", "GIGABYTE H610M"],
            "description": "Бюджетный вариант для офисных задач и легких игр."
        },
        "AMD Ryzen 5 5600": {
            "brand": "AMD",
            "socket": "AM4",
            "tpd": 65,
            "min_psu": 450,
            "motherboards": ["MSI B550M PRO-VDH", "ASRock B550M-HDV", "MSI B550M PRO"],
            "description": "Отличное соотношение цены и производительности. Идеален для игр."
        },
        "AMD Ryzen 7 5800X": {
            "brand": "AMD",
            "socket": "AM4",
            "tpd": 105,
            "min_psu": 600,
            "motherboards": ["GIGABYTE B550 AORUS ELITE", "ASUS TUF GAMING B550-PLUS", "MSI MAG B550 TOMAHAWK"],
            "description": "Мощный процессор для игр и профессиональных задач. 8 ядер."
        },
        "AMD Ryzen 5 7600": {
            "brand": "AMD",
            "socket": "AM5",
            "tpd": 65,
            "min_psu": 550,
            "motherboards": ["MSI B650M PRO-VDH", "ASUS TUF GAMING B650-PLUS", "GIGABYTE B650 AORUS ELITE"],
            "description": "Новое поколение AM5. Отличная производительность и поддержка DDR5."
        },
        "Intel Core i7-13700K": {
            "brand": "Intel",
            "socket": "LGA1700",
            "tpd": 125,
            "min_psu": 700,
            "motherboards": ["ASUS ROG MAXIMUS Z790 HERO", "GIGABYTE Z790 AORUS MASTER", "MSI MEG Z790 ACE"],
            "description": "Флагманский процессор для максимальной производительности."
        },
        "AMD Ryzen 9 5900X": {
            "brand": "AMD",
            "socket": "AM4",
            "tpd": 105,
            "min_psu": 650,
            "motherboards": ["ASUS ROG CROSSHAIR X570-E", "GIGABYTE X570 AORUS MASTER", "MSI MEG X570 UNIFY"],
            "description": "12 ядер для профессиональной работы и стриминга."
        }
    }

    # Видеокарты с энергопотреблением
    VIDEO_CARDS = {
        "NVIDIA GTX 1650": {"tpd": 75, "min_psu": 300, "recommended_psu": 450},
        "NVIDIA GTX 3060": {"tpd": 170, "min_psu": 550, "recommended_psu": 650},
        "NVIDIA RTX 4060": {"tpd": 115, "min_psu": 500, "recommended_psu": 600},
        "AMD Radeon RX 6600": {"tpd": 132, "min_psu": 500, "recommended_psu": 600},
        "NVIDIA RTX 4070 super": {"tpd": 220, "min_psu": 650, "recommended_psu": 750},
        "NVIDIA RTX 4080": {"tpd": 320, "min_psu": 750, "recommended_psu": 850},
        "NVIDIA RTX 4090": {"tpd": 450, "min_psu": 850, "recommended_psu": 1000}
    }

    # Оперативная память
    MEMORY_OPTIONS = [
        {"name": "8GB DDR4", "type": "DDR4", "speed": "3200MHz"},
        {"name": "16GB DDR4", "type": "DDR4", "speed": "3200MHz"},
        {"name": "32GB DDR4", "type": "DDR4", "speed": "3600MHz"},
        {"name": "16GB DDR5", "type": "DDR5", "speed": "6000MHz"},
        {"name": "32GB DDR5", "type": "DDR5", "speed": "6000MHz"}
    ]

    # Блоки питания
    POWER_SUPPLIES = [
        {"wattage": 500, "efficiency": "80+ Bronze", "price_category": "budget"},
        {"wattage": 650, "efficiency": "80+ Bronze", "price_category": "mid"},
        {"wattage": 750, "efficiency": "80+ Gold", "price_category": "premium"},
        {"wattage": 850, "efficiency": "80+ Gold", "price_category": "premium"},
        {"wattage": 1000, "efficiency": "80+ Platinum", "price_category": "high-end"}
    ]

    @staticmethod
    def get_processors_by_budget(budget):
        if budget == 800:
            return ["Intel Core i5-12400f", "AMD Ryzen 5 5600", "Intel Core i3-12100"]
        elif budget == 1200:
            return ["Intel Core i5-13600", "AMD Ryzen 7 5800X", "AMD Ryzen 5 7600"]
        elif budget == 2000:
            return ["Intel Core i7-13700K", "AMD Ryzen 9 5900X"]
        return []

    @staticmethod
    def get_videocards_by_budget(budget):
        if budget == 800:
            return ["NVIDIA GTX 1650", "NVIDIA GTX 3060", "AMD Radeon RX 6600"]
        elif budget == 1200:
            return ["NVIDIA RTX 4060", "NVIDIA RTX 3060", "AMD Radeon RX 6600"]
        elif budget == 2000:
            return ["NVIDIA RTX 4070 super", "NVIDIA RTX 4080"]
        return []

    @staticmethod
    def calculate_required_psu(processor_name, videocard_name):
        """Расчет минимального и рекомендуемого БП"""
        processor = ConfigLogic.PROCESSORS.get(processor_name, {"tpd": 100, "min_psu": 500})
        videocard = ConfigLogic.VIDEO_CARDS.get(videocard_name, {"tpd": 150, "min_psu": 500, "recommended_psu": 600})

        base_consumption = 100

        total_tpd = processor["tpd"] + videocard["tpd"] + base_consumption

        min_required = max(processor.get("min_psu", 500), videocard.get("min_psu", 500))

        recommended = int(total_tpd * 1.2)

        available_psus = [psu["wattage"] for psu in ConfigLogic.POWER_SUPPLIES]
        suitable_psus = [w for w in available_psus if w >= recommended]

        return {
            "min_required": min_required,
            "recommended": recommended,
            "suitable_options": sorted(suitable_psus),
            "total_consumption": total_tpd,
            "processor_tpd": processor["tpd"],
            "videocard_tpd": videocard["tpd"]
        }

    @staticmethod
    def get_processor_info(processor_name):
        return ConfigLogic.PROCESSORS.get(processor_name, {})

    @staticmethod
    def get_videocard_info(videocard_name):
        return ConfigLogic.VIDEO_CARDS.get(videocard_name, {})

    @staticmethod
    def get_configurations(budget):
        configurations = {
            800: [
                {
                    "processor": "Intel Core i5-12400f",
                    "videocard": "NVIDIA GTX 3060",
                    "memory": "16GB DDR4",
                    "motherboard": "GIGABYTE H610M",
                    "chipset": "H610M",
                    "price": 800,
                    "pros": "Хорошая производительность в играх.",
                    "cons": "Ограниченные возможности для апгрейда.",
                    "description": "Идеальная сборка для геймеров, которые хотят получить хорошую производительность в играх на средних настройках.",
                    "power_supply": "650W"
                },
                {
                    "processor": "AMD Ryzen 5 5600",
                    "videocard": "NVIDIA rtx3060",
                    "memory": "16GB DDR4",
                    "motherboard": "MSI B550M PRO-VDH",
                    "chipset": "B550",
                    "price": 750,
                    "pros": "Отличная цена/производительность.",
                    "cons": "Ограниченная производительность в графически требовательных играх.",
                    "description": "Бюджетная сборка с отличным соотношением цены и производительности.",
                    "power_supply": "650W"
                },
                {
                    "processor": "Intel Core i3-12100",
                    "videocard": "NVIDIA GTX 1650",
                    "memory": "8GB DDR4",
                    "motherboard": "ASUS PRIME H610M-A",
                    "chipset": "H610",
                    "price": 600,
                    "pros": "Бюджетная сборка для офисных задач.",
                    "cons": "Не подходит для современных игр.",
                    "description": "Подходит для офисных задач и легких игр.",
                    "power_supply": "500W"
                },
                {
                    "processor": "AMD Athlon 3000G",
                    "videocard": "Integrated Vega 3",
                    "memory": "8GB DDR4",
                    "motherboard": "ASRock A320M-HDV",
                    "chipset": "A320",
                    "price": 350,
                    "pros": "Очень низкая цена.",
                    "cons": "Слабая производительность.",
                    "description": "Минимальная сборка для базовых задач.",
                    "power_supply": "300W"
                },
                {
                    "processor": "Intel Pentium Gold G6400",
                    "videocard": "NVIDIA GTX 1650",
                    "memory": "8GB DDR4",
                    "motherboard": "Gigabyte H410M",
                    "chipset": "H410",
                    "price": 400,
                    "pros": "Хорошая производительность для базовых задач.",
                    "cons": "Не подходит для серьезных игр.",
                    "description": "Подходит для офисных задач и легких игр.",
                    "power_supply": "500W"
                },
                {
                    "processor": "AMD Ryzen 3 3200G",
                    "videocard": "Integrated Vega 8",
                    "memory": "16GB DDR4",
                    "motherboard": "MSI A320M PRO-VDH",
                    "chipset": "A320",
                    "price": 450,
                    "pros": "Подходит для легких игр.",
                    "cons": "Не хватает мощности для современных игр.",
                    "description": "Подходит для легких игр и офисных задач.",
                    "power_supply": "500W"
                }
            ],
            1200: [
                {
                    "processor": "Intel Core i5-13600",
                    "videocard": "NVIDIA RTX 4060",
                    "memory": "16GB DDR4",
                    "motherboard": "GIGABYTE B760 DS3H DDR4",
                    "chipset": "B760",
                    "price": 1150,
                    "pros": "Высокая производительность в играх и многопоточности.",
                    "cons": "Высокая цена, потребление энергии.",
                    "description": "Сборка для геймеров, которые хотят получить максимальную производительность в играх.",
                    "power_supply": "750W"
                },
                {
                    "processor": "AMD Ryzen 7 5800X",
                    "videocard": "AMD Radeon RX 6800 XT",
                    "memory": "16GB DDR4",
                    "motherboard": "GIGABYTE B550 AORUS ELITE",
                    "chipset": "B550",
                    "price": 1200,
                    "pros": "Отличная производительность в многопоточности.",
                    "cons": "Может перегреваться без хорошего охлаждения.",
                    "description": "Сборка для геймеров и профессионалов, которые хотят получить максимальную производительность.",
                    "power_supply": "750W"
                },
                {
                    "processor": "AMD Ryzen 5 7500f ",
                    "videocard": " NVIDIA RTX 4060",
                    "memory": "16GB DDR4",
                    "motherboard": "GIGABYTE B650 EAGLE AX",
                    "chipset": "B550",
                    "price": 1200,
                    "pros": "Отличная производительность в многопоточности.",
                    "cons": "можно использовать стоковое охлаждение.",
                    "description": "Сборка для геймеров, которые хотят получить хорошую производительность в играх.",
                    "power_supply": "650W"
                },
                {
                    "processor": "Intel Core i5-12400",
                    "videocard": "NVIDIA GTX 1660 Super",
                    "memory": "16GB DDR4",
                    "motherboard": "ASUS TUF Gaming B560M-PLUS",
                    "chipset": "B560",
                    "price": 1100,
                    "pros": "Хорошая производительность в играх.",
                    "cons": "Не поддерживает DDR5.",
                    "description": "Сборка для геймеров, которые хотят получить хорошую производительность в играх.",
                    "power_supply": "650W"
                },
                {
                    "processor": "AMD Ryzen 5 7600",
                    "videocard": "NVIDIA RTX 3060 Ti",
                    "memory": "16GB DDR5",
                    "motherboard": "MSI B650M PRO-VDH",
                    "chipset": "B650",
                    "price": 1200,
                    "pros": "Отличная производительность в играх и приложениях.",
                    "cons": "Высокая цена на видеокарту.",
                    "description": "Сборка для геймеров, которые хотят получить максимальную производительность в играх.",
                    "power_supply": "750W"
                },
                {
                    "processor": "Intel Core i5-12400F",
                    "videocard": "AMD Radeon RX 6600",
                    "memory": "16GB DDR4",
                    "motherboard": "MSI PRO B660M-A",
                    "chipset": "B660",
                    "price": 1150,
                    "pros": "Отличная производительность в играх.",
                    "cons": "Ограниченные возможности для апгрейда.",
                    "description": "Сборка для геймеров, которые хотят получить хорошую производительность в играх.",
                    "power_supply": "650W"
                }
            ],
            2000: [
                {
                    "processor": "Intel Core i7-13700K",
                    "videocard": "NVIDIA RTX 4070 super",
                    "memory": "32GB DDR5",
                    "motherboard": " MSI PRO Z790-A",
                    "chipset": "Z790",
                    "price": 1900,
                    "pros": "Выдающаяся производительность в играх и приложениях.",
                    "cons": "Высокая цена, потребление энергии.",
                    "description": "Сборка для геймеров и профессионалов, которые хотят получить максимальную производительность.",
                    "power_supply": "850W"
                },
                {
                    "processor": "AMD Ryzen 9 5900X",
                    "videocard": "NVIDIA RTX 4070 super",
                    "memory": "32GB DDR4",
                    "motherboard": "MSI MAG X570 TOMAHAWK",
                    "chipset": "X570",
                    "price": 2000,
                    "pros": "Отличная производительность в многозадачности и играх.",
                    "cons": "Высокая стоимость, требует хорошего охлаждения.",
                    "description": "Сборка для геймеров и профессионалов, которые хотят получить максимальную производительность.",
                    "power_supply": "850W"
                },
                {
                    "processor": "Intel Core i9-12900K",
                    "videocard": "NVIDIA RTX 4080",
                    "memory": "32GB DDR5",
                    "motherboard": "ASUS ROG STRIX Z690-E",
                    "chipset": "Z690",
                    "price": 2000,
                    "pros": "Максимальная производительность для игр и работы.",
                    "cons": "Очень высокая цена.",
                    "description": "Сборка для геймеров и профессионалов, которые хотят получить максимальную производительность.",
                    "power_supply": "1000W"
                },
                {
                    "processor": "AMD Ryzen 7 5800X3D",
                    "videocard": "AMD Radeon RX 6800 XT",
                    "memory": "32GB DDR4",
                    "motherboard": "ASRock X570 Taichi",
                    "chipset": "X570",
                    "price": 2000,
                    "pros": "Отличная производительность в играх и приложениях.",
                    "cons": "Высокая цена, требует качественного охлаждения.",
                    "description": "Сборка для геймеров и профессионалов, которые хотят получить максимальную производительность.",
                    "power_supply": "850W"
                },
                {
                    "processor": "Intel Core i7-12700K",
                    "videocard": "NVIDIA RTX 4070",
                    "memory": "32GB DDR5",
                    "motherboard": "GIGABYTE Z690 AORUS ELITE",
                    "chipset": "Z690",
                    "price": 2000,
                    "pros": "Отличная производительность в играх и многозадачности.",
                    "cons": "Высокая стоимость.",
                    "description": "Сборка для геймеров и профессионалов, которые хотят получить максимальную производительность.",
                    "power_supply": "850W"
                },
                {
                    "processor": "AMD Ryzen 9 7900X",
                    "videocard": "NVIDIA RTX 4070 Ti",
                    "memory": "32GB DDR5",
                    "motherboard": "ASUS ROG STRIX B650E-F",
                    "chipset": "B650E",
                    "price": 2000,
                    "pros": "Идеально подходит для работы и игр.",
                    "cons": "Высокая цена.",
                    "description": "Сборка для геймеров и профессионалов, которые хотят получить максимальную производительность.",
                    "power_supply": "850W"
                }
            ],
            float('inf'): [
                {
                    "processor": "Intel Core i7-13700K",
                    "videocard": "NVIDIA RTX 4080",
                    "memory": "64GB DDR5",
                    "motherboard": "ASUS ROG MAXIMUS Z690 HERO",
                    "chipset": "Z690",
                    "price": 3000,
                    "pros": "Максимальная производительность, отличная для игр и работы.",
                    "cons": "Очень высокая цена.",
                    "description": "Сборка для геймеров и профессионалов, которые хотят получить максимальную производительность.",
                    "power_supply": "1000W"
                },
                {
                    "processor": "AMD Ryzen 9 7950X",
                    "videocard": "NVIDIA RTX 4090",
                    "memory": "64GB DDR5",
                    "motherboard": " ASUS TUF GAMING B650-PLUS",
                    "chipset": "B650",
                    "price": 4000,
                    "pros": "Выдающаяся производительность, отличная для профессиональной работы.",
                    "cons": "Высокая цена, требует качественного охлаждения, желательно водяное 3 секционное",
                    "description": "Сборка для геймеров и профессионалов, которые хотят получить максимальную производительность.",
                    "power_supply": "1000W"
                },
                {
                    "processor": "Intel Core i9-13900K",
                    "videocard": "NVIDIA RTX 4090",
                    "memory": "64GB DDR5",
                    "motherboard": "MSI MEG Z690 UNIFY",
                    "chipset": "Z690",
                    "price": 4500,
                    "pros": "Лучшая производительность на данный момент.",
                    "cons": "Очень высокая цена.",
                    "description": "Сборка для геймеров и профессионалов, которые хотят получить максимальную производительность.",
                    "power_supply": "1000W"
                },
                {
                    "processor": "AMD Ryzen 9 7950X3D",
                    "videocard": "NVIDIA RTX 4080 Ti",
                    "memory": "64GB DDR5",
                    "motherboard": "ASUS ROG CROSSHAIR X670E HERO",
                    "chipset": "X670E",
                    "price": 4800,
                    "pros": "Отличная производительность в играх и приложениях.",
                    "cons": "Высокая цена, требует качественного охлаждения.",
                    "description": "Сборка для геймеров и профессионалов, которые хотят получить максимальную производительность.",
                    "power_supply": "1000W"
                },
                {
                    "processor": "Intel Core i9-14900KS",
                    "videocard": "NVIDIA RTX 4090",
                    "memory": "128GB DDR5",
                    "motherboard": "ASUS ROG MAXIMUS Z790 EXTREME",
                    "chipset": "Z690",
                    "price": 5000,
                    "pros": "Максимальная производительность для игр и профессиональной работы.",
                    "cons": "Очень высокая цена.",
                    "description": "Сборка для геймеров и профессионалов, которые хотят получить максимальную производительность.",
                    "power_supply": "1000W"
                },
                {
                    "processor": "AMD Ryzen Threadripper 5990X",
                    "videocard": "NVIDIA RTX 4090",
                    "memory": "128GB DDR5",
                    "motherboard": "ASUS ROG ZENITH II EXTREME",
                    "chipset": "TRX40",
                    "price": 6000,
                    "pros": "Идеально подходит для профессионального использования и игр.",
                    "cons": "Экстремально высокая цена.",
                    "description": "Сборка для геймеров и профессионалов, которые хотят получить максимальную производительность.",
                    "power_supply": "1200W"
                }
            ]
        }
        return configurations.get(budget, [])