import traceback
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QMessageBox, QTextEdit, QHBoxLayout, \
    QProgressBar, QMenu, QAction, QDesktopWidget, QApplication

from building_manager import BuildingManager, ResourceExtractor, PowerPlant, Farm
from population import Population
from resource_manager import ResourceManager


def create_label(text, font, layout):
    label = QLabel(text)
    label.setFont(font)
    layout.addWidget(label)
    return label


def create_button(text, font, layout, callback):
    button = QPushButton(text)
    button.setFont(font)
    button.clicked.connect(callback)
    layout.addWidget(button)
    return button


class GalacticPioneers(QMainWindow):
    RESEARCH_TIME_TOTAL = 60  # Total time for research in seconds

    def __init__(self):
        super().__init__()
        self.totalEnergyConsumption = None
        self.no_food_counter = 0
        self.eventLog = None
        self.researchProgress = None
        self.researchButton = None
        self.researchUpgradeButton = None
        self.buildFarmButton = None
        self.buildPowerPlantButton = None
        self.buildMinerButton = None
        self.foodProductionLabel = None
        self.farmsCountLabel = None
        self.powerPlantProductionLabel = None
        self.powerPlantCountLabel = None
        self.minerProductionLabel = None
        self.minerCountLabel = None
        self.populationLabel = None
        self.researchPointsLabel = None
        self.foodLabel = None
        self.energyLabel = None
        self.mineralsLabel = None
        self.currencyLabel = None
        self.researchTimer = None
        self.updateTimer = None
        self.researchTimeRemaining = None
        self.population = None
        self.buildingManager = None
        self.resourceManager = None
        self.totalEnergyConsumptionLabel = None
        self.init_resources()
        self.init_ui()
        self.start_resource_update_timer()

    def log_event(self, message):
        """ Append a message to the event log. """
        if self.eventLog is not None:
            self.eventLog.append(message)

    def init_resources(self):
        self.resourceManager = ResourceManager()
        self.buildingManager = BuildingManager()
        self.population = Population(initial_size=100, growth_rate=0.02)
        self.researchTimeRemaining = self.RESEARCH_TIME_TOTAL

    def start_resource_update_timer(self):
        self.updateTimer = QTimer(self)
        self.updateTimer.timeout.connect(self.update_resources_wrapper)
        self.updateTimer.start(1000)  # Update resources every second

    def update_resources_wrapper(self):
        self.resourceManager.update_resources(self.buildingManager, self.population, self.log_event, self.update_labels)

    def init_ui(self):
        self.setWindowTitle('Galactic Pioneers')
        self.setGeometry(300, 300, 1000, 800)
        font = QFont("Arial", 12, QFont.Bold)

        # Menu Bar
        menu_bar = self.menuBar()
        file_menu = QMenu('File', self)
        exit_action = QAction('Exit', self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        menu_bar.addMenu(file_menu)

        edit_menu = QMenu('Edit', self)
        menu_bar.addMenu(edit_menu)

        help_menu = QMenu('Help', self)
        menu_bar.addMenu(help_menu)

        # Central Widget
        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)
        mainLayout = QHBoxLayout(centralWidget)

        leftPanel = self.create_resource_panel(font)
        rightPanel = self.create_building_panel(font)
        bottomPanel = self.create_action_panel(font)

        mainLayout.addLayout(leftPanel)
        mainLayout.addLayout(rightPanel)
        mainLayout.addLayout(bottomPanel)

        self.researchTimer = QTimer(self)
        self.researchTimer.timeout.connect(self.update_research)

        self.show()

        # Center the window on the screen
        screen = QApplication.screens()[0]
        screen_center = screen.geometry().center()
        frame_geometry = self.frameGeometry()
        frame_geometry.moveCenter(screen_center)
        self.move(frame_geometry.topLeft())

    def create_resource_panel(self, font):
        layout = QVBoxLayout()
        self.currencyLabel = create_label('Currency: 0', font, layout)
        self.mineralsLabel = create_label('Minerals: 0', font, layout)
        self.energyLabel = create_label('Energy: 0', font, layout)
        self.foodLabel = create_label('Food: 0', font, layout)
        self.researchPointsLabel = create_label('Research Points: 0', font, layout)
        self.populationLabel = create_label('Population: 0', font, layout)
        return layout

    def create_building_panel(self, font):
        layout = QVBoxLayout()
        self.minerCountLabel = create_label('Miners: 0', font, layout)
        self.minerProductionLabel = create_label('Mineral Production Rate: 0/s', font, layout)
        self.powerPlantCountLabel = create_label('Power Plants: 0', font, layout)
        self.powerPlantProductionLabel = create_label('Energy Production Rate: 0/s', font, layout)
        self.totalEnergyConsumptionLabel = create_label('Total Energy Consumption: 0/s', font, layout)
        self.farmsCountLabel = create_label('Farms: 0', font, layout)
        self.foodProductionLabel = create_label('Food Production Rate: 0/s', font, layout)
        return layout

    def create_action_panel(self, font):
        layout = QVBoxLayout()
        self.buildMinerButton = create_button('Build Miner', font, layout, self.build_miner)
        self.buildPowerPlantButton = create_button('Build Power Plant', font, layout, self.build_power_plant)
        self.buildFarmButton = create_button('Build Farm', font, layout, self.build_farm)
        self.researchUpgradeButton = create_button('Purchase Upgrade', font, layout, self.research_upgrade)
        self.researchButton = create_button('Start Research', font, layout, self.on_research)
        self.researchProgress = QProgressBar(self)
        self.researchProgress.setAlignment(Qt.AlignCenter)
        self.researchProgress.setValue(0)
        layout.addWidget(self.researchProgress)
        self.eventLog = QTextEdit()
        self.eventLog.setReadOnly(True)
        self.eventLog.setFont(QFont("Arial", 10))
        layout.addWidget(self.eventLog)
        return layout

    def build_miner(self):
        miner_cost = 100
        miner_output = ResourceExtractor('minerals', 5)  # Example generation rate
        if self.resourceManager.spend_resource('minerals', miner_cost):
            self.buildingManager.add_extractor(miner_output)
            self.eventLog.append("Miner built.")
            self.update_labels()
        else:
            QMessageBox.warning(self, 'Insufficient Funds', 'You do not have enough minerals to build a miner.')

    def build_power_plant(self):
        power_plant_cost = 100
        power_plant_output = PowerPlant(10)
        if self.resourceManager.spend_resource('minerals', power_plant_cost):
            self.buildingManager.add_power_plant(power_plant_output)
            self.eventLog.append("Power plant built.")
            self.update_labels()
        else:
            QMessageBox.warning(self, 'Insufficient Funds', 'You do not have enough minerals to build a power plant.')

    def build_farm(self):
        farm_cost = 100
        food_production_rate = 10
        if self.resourceManager.spend_resource('minerals', farm_cost):
            farm = Farm(food_production_rate)
            self.buildingManager.add_farm(farm)
            self.eventLog.append("Farm built.")
            self.update_labels()
        else:
            QMessageBox.warning(self, 'Insufficient Funds', 'You do not have enough minerals to build a farm.')

    def research_upgrade(self):
        if self.resourceManager.spend_resource('researchPoints', 20):
            for miner in self.buildingManager.extractors:
                miner.generation_rate += 1
            for plant in self.buildingManager.power_plants:
                plant.energy_output += 5
            self.eventLog.append("Research upgrade applied.")
            self.update_labels()
        else:
            QMessageBox.warning(self, 'Insufficient Research Points',
                                'You do not have enough research points for this upgrade.')

    def on_research(self):
        if self.resourceManager.spend_resource('currency', 100):
            self.update_labels()
            self.researchButton.setDisabled(True)
            self.researchProgress.setValue(0)
            self.researchTimeRemaining = self.RESEARCH_TIME_TOTAL * 100
            self.researchTimer.start(10)
        else:
            QMessageBox.warning(self, 'Insufficient Funds', 'You do not have enough currency to start research.')

    def update_research(self):
        try:
            self.researchTimeRemaining -= 1
            progress_value = ((self.RESEARCH_TIME_TOTAL * 100 - self.researchTimeRemaining) / (
                        self.RESEARCH_TIME_TOTAL * 100)) * 100
            self.researchProgress.setValue(int(progress_value))

            if self.researchTimeRemaining <= 0:
                self.researchTimer.stop()
                self.researchButton.setDisabled(False)
                self.researchProgress.setValue(100)
                self.resourceManager.resources['researchPoints'] += 10
                self.update_labels()
        except Exception as e:
            print("Error during research update:", str(e))
            traceback.print_exc()

    def update_labels(self):
        self.currencyLabel.setText(f'Currency: {self.resourceManager.resources["currency"]}')
        self.mineralsLabel.setText(f'Minerals: {self.resourceManager.resources["minerals"]}')
        self.energyLabel.setText(f'Energy: {self.resourceManager.resources["energy"]}')
        self.foodLabel.setText(f'Food: {self.resourceManager.resources["food"]}')
        self.researchPointsLabel.setText(f'Research Points: {self.resourceManager.resources["researchPoints"]}')
        self.minerCountLabel.setText(f'Miners: {len(self.buildingManager.extractors)}')
        self.minerProductionLabel.setText(
            f'Mineral Production Rate: {self.buildingManager.total_resource_production()}/s')
        self.powerPlantCountLabel.setText(f'Power Plants: {len(self.buildingManager.power_plants)}')
        self.powerPlantProductionLabel.setText(
            f'Energy Production Rate: {self.buildingManager.total_energy_production()}/s')
        self.farmsCountLabel.setText(f'Farms: {len(self.buildingManager.farms)}')
        self.foodProductionLabel.setText(f'Food Production Rate: {self.buildingManager.total_food_production()}/s')
        self.populationLabel.setText(f'Population: {self.population.size}')
        self.totalEnergyConsumptionLabel.setText(f'Total Energy Consumption: {self.totalEnergyConsumption}/s')
