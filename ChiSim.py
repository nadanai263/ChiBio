import copy
import time
from datetime import datetime, date
from threading import Thread, Lock

######################################
#Initialise data structures.
######################################

#Sysdata is a structure created for each device and contains the setup / measured data related to that device during an experiment. All of this information is passed into the user interface during an experiment.
sysData = {'M0' : {
   'UIDevice' : 'M0',
   'present' : 0,
   'presentDevices' : { 'M0' : 0,'M1' : 0,'M2' : 0,'M3' : 0,'M4' : 0,'M5' : 0,'M6' : 0,'M7' : 0},
   'Version' : {'value' : 'Turbidostat V3.0'},
   'DeviceID' : '',
   'time' : {'record' : []},
   'LEDA' : {'WL' : '395', 'default': 0.1, 'target' : 0.0, 'max': 1.0, 'min' : 0.0,'ON' : 0},
   'LEDB' : {'WL' : '457', 'default': 0.1, 'target' : 0.0, 'max': 1.0, 'min' : 0.0,'ON' : 0},
   'LEDC' : {'WL' : '500', 'default': 0.1, 'target' : 0.0, 'max': 1.0, 'min' : 0.0,'ON' : 0},
   'LEDD' : {'WL' : '523', 'default': 0.1, 'target' : 0.0, 'max': 1.0, 'min' : 0.0,'ON' : 0},
   'LEDE' : {'WL' : '595', 'default': 0.1, 'target' : 0.0, 'max': 1.0, 'min' : 0.0,'ON' : 0},
   'LEDF' : {'WL' : '623', 'default': 0.1, 'target' : 0.0, 'max': 1.0, 'min' : 0.0,'ON' : 0},
   'LEDG' : {'WL' : '6500K', 'default': 0.1, 'target' : 0.0, 'max': 1.0, 'min' : 0.0,'ON' : 0},
   'LASER650' : {'name' : 'LASER650', 'default': 0.5, 'target' : 0.0, 'max': 1.0, 'min' : 0.0,'ON' : 0},
   'UV' : {'WL' : 'UV', 'default': 0.5, 'target' : 0.0, 'max': 1.0, 'min' : 0.0,'ON' : 0},
   'Heat' : {'default': 0.0, 'target' : 0.0, 'max': 1.0, 'min' : 0.0,'ON' : 0,'record' : []},
   'Thermostat' : {'default': 37.0, 'target' : 0.0, 'max': 50.0, 'min' : 0.0,'ON' : 0,'record' : [],'cycleTime' : 30.0, 'Integral' : 0.0,'last' : -1},
   'Experiment' : {'indicator' : 'USR0', 'startTime' : 'Waiting', 'startTimeRaw' : 0, 'ON' : 0,'cycles' : 0, 'cycleTime' : 60.0,'threadCount' : 0},
   'Terminal' : {'text' : ''},
   'AS7341' : {
        'spectrum' : {'nm410' : 0, 'nm440' : 0, 'nm470' : 0, 'nm510' : 0, 'nm550' : 0, 'nm583' : 0, 'nm620' : 0, 'nm670' : 0,'CLEAR' : 0, 'NIR' : 0,'DARK' : 0,'ExtGPIO' : 0, 'ExtINT' : 0, 'FLICKER' : 0},
        'channels' : {'nm410' : 0, 'nm440' : 0, 'nm470' : 0, 'nm510' : 0, 'nm550' : 0, 'nm583' : 0, 'nm620' : 0, 'nm670' : 0,'CLEAR' : 0, 'NIR' : 0,'DARK' : 0,'ExtGPIO' : 0, 'ExtINT' : 0, 'FLICKER' : 0},
        'current' : {'ADC0': 0,'ADC1': 0,'ADC2': 0,'ADC3': 0,'ADC4': 0,'ADC5' : 0}},
   'ThermometerInternal' : {'current' : 0.0,'record' : []},
   'ThermometerExternal' : {'current' : 0.0,'record' : []},
   'ThermometerIR' : {'current' : 0.0,'record' : []},
   'OD' :  {'current' : 0.0,'target' : 0.5,'default' : 0.5,'max': 10, 'min' : 0,'record' : [],'targetrecord' : [],'Measuring' : 0, 'ON' : 0,'Integral' : 0.0,'Integral2' : 0.0,'device' : 'LASER650'},
   'OD0' : {'target' : 0.0,'raw' : 0.0,'max' : 100000.0,'min': 0.0,'LASERb' : 1.833 ,'LASERa' : 0.226, 'LEDFa' : 0.673, 'LEDAa' : 7.0  },
   'Chemostat' : {'ON' : 0, 'p1' : 0.0, 'p2' : 0.1},
   'Zigzag': {'ON' : 0, 'Zig' : 0.04,'target' : 0.0,'SwitchPoint' : 0},
   'GrowthRate': {'current' : 0.0,'record' : [],'default' : 2.0},
   'Volume' : {'target' : 20.0,'max' : 50.0, 'min' : 0.0,'ON' : 0},
   'Pump1' :  {'target' : 0.0,'default' : 0.0,'max': 1.0, 'min' : -1.0, 'direction' : 1.0, 'ON' : 0,'record' : [], 'thread' : 0},
   'Pump2' :  {'target' : 0.0,'default' : 0.0,'max': 1.0, 'min' : -1.0, 'direction' : 1.0, 'ON' : 0,'record' : [], 'thread' : 0},
   'Pump3' :  {'target' : 0.0,'default' : 0.0,'max': 1.0, 'min' : -1.0, 'direction' : 1.0, 'ON' : 0,'record' : [], 'thread' : 0},
   'Pump4' :  {'target' : 0.0,'default' : 0.0,'max': 1.0, 'min' : -1.0, 'direction' : 1.0, 'ON' : 0,'record' : [], 'thread' : 0},
   'Stir' :  {'target' : 0.0,'default' : 0.5,'max': 1.0, 'min' : 0.0, 'ON' : 0},
   'Light' :  {'target' : 0.0,'default' : 0.5,'max': 1.0, 'min' : 0.0, 'ON' : 0, 'Excite' : 'LEDD', 'record' : []},
   'Custom' :  {'Status' : 0.0,'default' : 0.0,'Program': 'C1', 'ON' : 0,'param1' : 0, 'param2' : 0, 'param3' : 0.0, 'record' : []},
   'FP1' : {'ON' : 0 ,'LED' : 0,'BaseBand' : 0, 'Emit11Band' : 0,'Emit2Band' : 0,'Base' : 0, 'Emit11' : 0,'Emit2' : 0,'BaseRecord' : 0, 'Emit1Record' : 0,'Emit2Record' : 0 ,'Gain' : 0},
   'FP2' : {'ON' : 0 ,'LED' : 0,'BaseBand' : 0, 'Emit11Band' : 0,'Emit2Band' : 0,'Base' : 0, 'Emit11' : 0,'Emit2' : 0,'BaseRecord' : 0, 'Emit1Record' : 0,'Emit2Record' : 0 ,'Gain' : 0},
   'FP3' : {'ON' : 0 ,'LED' : 0,'BaseBand' : 0, 'Emit11Band' : 0,'Emit2Band' : 0,'Base' : 0, 'Emit11' : 0,'Emit2' : 0,'BaseRecord' : 0, 'Emit1Record' : 0,'Emit2Record' : 0 ,'Gain' : 0},
   'biofilm' : {'LEDA' : {'nm410' : 0, 'nm440' : 0, 'nm470' : 0, 'nm510' : 0, 'nm550' : 0, 'nm583' : 0, 'nm620' : 0, 'nm670' : 0,'CLEAR' : 0,'NIR' : 0},
                'LEDB' : {'nm410' : 0, 'nm440' : 0, 'nm470' : 0, 'nm510' : 0, 'nm550' : 0, 'nm583' : 0, 'nm620' : 0, 'nm670' : 0,'CLEAR' : 0,'NIR' : 0},
                'LEDC' : {'nm410' : 0, 'nm440' : 0, 'nm470' : 0, 'nm510' : 0, 'nm550' : 0, 'nm583' : 0, 'nm620' : 0, 'nm670' : 0,'CLEAR' : 0,'NIR' : 0},
                'LEDD' : {'nm410' : 0, 'nm440' : 0, 'nm470' : 0, 'nm510' : 0, 'nm550' : 0, 'nm583' : 0, 'nm620' : 0, 'nm670' : 0,'CLEAR' : 0,'NIR' : 0},
                'LEDE' : {'nm410' : 0, 'nm440' : 0, 'nm470' : 0, 'nm510' : 0, 'nm550' : 0, 'nm583' : 0, 'nm620' : 0, 'nm670' : 0,'CLEAR' : 0,'NIR' : 0},
                'LEDF' : {'nm410' : 0, 'nm440' : 0, 'nm470' : 0, 'nm510' : 0, 'nm550' : 0, 'nm583' : 0, 'nm620' : 0, 'nm670' : 0,'CLEAR' : 0,'NIR' : 0},
                'LEDG' : {'nm410' : 0, 'nm440' : 0, 'nm470' : 0, 'nm510' : 0, 'nm550' : 0, 'nm583' : 0, 'nm620' : 0, 'nm670' : 0,'CLEAR' : 0,'NIR' : 0},
                'LASER650' : {'nm410' : 0, 'nm440' : 0, 'nm470' : 0, 'nm510' : 0, 'nm550' : 0, 'nm583' : 0, 'nm620' : 0, 'nm670' : 0,'CLEAR' : 0,'NIR' : 0}}
   }}



#SysDevices is unique to each device and is responsible for storing information required for the digital communications, and various automation funtions. These values are stored outside sysData since they are not passable into the HTML interface using the jsonify package.        
sysDevices = {'M0' : {
    'AS7341' : {'device' : 0},
    'ThermometerInternal' : {'device' : 0},
    'ThermometerExternal' : {'device' : 0},
    'ThermometerIR' : {'device' : 0,'address' :0},
    'DAC' : {'device' : 0},
    'Pumps' : {'device' : 0,'startup' : 0, 'frequency' : 0},
    'PWM' : {'device' : 0,'startup' : 0, 'frequency' : 0},
    'Pump1' : {'thread' : 0,'threadCount' : 0, 'active' : 0},
    'Pump2' : {'thread' : 0,'threadCount' : 0, 'active' : 0},
    'Pump3' : {'thread' : 0,'threadCount' : 0, 'active' : 0},
    'Pump4' : {'thread' : 0,'threadCount' : 0, 'active' : 0},
    'Experiment' : {'thread' : 0},
    'Thermostat' : {'thread' : 0,'threadCount' : 0},
    
}}


for M in ['M1','M2','M3','M4','M5','M6','M7']:
        sysData[M]=copy.deepcopy(sysData['M0'])
        sysDevices[M]=copy.deepcopy(sysDevices['M0'])
        

#sysItems stores information about digital addresses which is used as a reference for all devices.        
sysItems = {
    'DAC' : {'LEDA' : '00000100','LEDB' : '00000000','LEDC' : '00000110','LEDD' : '00000001','LEDE' : '00000101','LEDF' : '00000011','LEDG' : '00000010','LASER650' : '00000111'},
    'Multiplexer' : {'device' : 0 , 'M0' : '00000001','M1' : '00000010','M2' : '00000100','M3' : '00001000','M4' : '00010000','M5' : '00100000','M6' : '01000000','M7' : '10000000'},
    'UIDevice' : 'M0',
    'Watchdog' : {'pin' : 'P8_11','thread' : 0,'ON' : 1},
    'FailCount' : 0,
    'All' : {'ONL' : 0xFA, 'ONH' : 0xFB, 'OFFL' : 0xFC, 'OFFH' : 0xFD},
    'Stir' : {'ONL' : 0x06, 'ONH' : 0x07, 'OFFL' : 0x08, 'OFFH' : 0x09},
    'Heat' : {'ONL' : 0x3E, 'ONH' : 0x3F, 'OFFL' : 0x40, 'OFFH' : 0x41},
    'UV' : {'ONL' : 0x42, 'ONH' : 0x43, 'OFFL' : 0x44, 'OFFH' : 0x45},
    'LEDA' : {'ONL' : 0x0E, 'ONH' : 0x0F, 'OFFL' : 0x10, 'OFFH' : 0x11},
    'LEDB' : {'ONL' : 0x16, 'ONH' : 0x17, 'OFFL' : 0x18, 'OFFH' : 0x19},
    'LEDC' : {'ONL' : 0x0A, 'ONH' : 0x0B, 'OFFL' : 0x0C, 'OFFH' : 0x0D},
    'LEDD' : {'ONL' : 0x1A, 'ONH' : 0x1B, 'OFFL' : 0x1C, 'OFFH' : 0x1D},
    'LEDE' : {'ONL' : 0x22, 'ONH' : 0x23, 'OFFL' : 0x24, 'OFFH' : 0x25},
    'LEDF' : {'ONL' : 0x1E, 'ONH' : 0x1F, 'OFFL' : 0x20, 'OFFH' : 0x21},
    'LEDG' : {'ONL' : 0x12, 'ONH' : 0x13, 'OFFL' : 0x14, 'OFFH' : 0x15},
    'Pump1' : {
        'In1' : {'ONL' : 0x06, 'ONH' : 0x07, 'OFFL' : 0x08, 'OFFH' : 0x09},
        'In2' : {'ONL' : 0x0A, 'ONH' : 0x0B, 'OFFL' : 0x0C, 'OFFH' : 0x0D},
    },
    'Pump2' : {
        'In1' : {'ONL' : 0x0E, 'ONH' : 0x0F, 'OFFL' : 0x10, 'OFFH' : 0x11},
        'In2' : {'ONL' : 0x12, 'ONH' : 0x13, 'OFFL' : 0x14, 'OFFH' : 0x15},
    },
    'Pump3' : {
        'In1' : {'ONL' : 0x16, 'ONH' : 0x17, 'OFFL' : 0x18, 'OFFH' : 0x19},
        'In2' : {'ONL' : 0x1A, 'ONH' : 0x1B, 'OFFL' : 0x1C, 'OFFH' : 0x1D},
    },
    'Pump4' : {
        'In1' : {'ONL' : 0x1E, 'ONH' : 0x1F, 'OFFL' : 0x20, 'OFFH' : 0x21},
        'In2' : {'ONL' : 0x22, 'ONH' : 0x23, 'OFFL' : 0x24, 'OFFH' : 0x25},
    },
    'AS7341' : {
        '0x00' : {'A' : 'nm470', 'B' : 'U'},
        '0x01' : {'A' : 'U', 'B' : 'nm410'},
        '0x02' : {'A' : 'U', 'B' : 'U'},
        '0x03' : {'A' : 'nm670', 'B' : 'U'},
        '0x04' : {'A' : 'U', 'B' : 'nm583'},
        '0x05' : {'A' : 'nm510', 'B' : 'nm440'},
        '0x06' : {'A' : 'nm550', 'B' : 'U'},
        '0x07' : {'A' : 'U', 'B' : 'nm620'},
        '0x08' : {'A' : 'CLEAR', 'B' : 'U'},
        '0x09' : {'A' : 'nm550', 'B' : 'U'},
        '0x0A' : {'A' : 'U', 'B' : 'nm620'},
        '0x0B' : {'A' : 'U', 'B' : 'U'},
        '0x0C' : {'A' : 'nm440', 'B' : 'U'},
        '0x0D' : {'A' : 'U', 'B' : 'nm510'},
        '0x0E' : {'A' : 'nm583', 'B' : 'nm670'},
        '0x0F' : {'A' : 'nm470', 'B' : 'U'},
        '0x10' : {'A' : 'ExtGPIO', 'B' : 'nm410'},
        '0x11' : {'A' : 'CLEAR', 'B' : 'ExtINT'},
        '0x12' : {'A' : 'DARK', 'B' : 'U'},
        '0x13' : {'A' : 'FLICKER', 'B' : 'NIR'},
    }
}


######################################
# Initialisation functions
######################################


def initialise(M):
    #Function that initialises all parameters / clears stored values for a given device.
    #If you want to record/add values to sysData, recommend adding an initialisation line in here.
    global sysData;
    global sysItems;
    global sysDevices

    for LED in ['LEDA','LEDB','LEDC','LEDD','LEDE','LEDF','LEDG']:
        sysData[M][LED]['target']=sysData[M][LED]['default']
        sysData[M][LED]['ON']=0
    
    sysData[M]['UV']['target']=sysData[M]['UV']['default']
    sysData[M]['UV']['ON']=0
    
    sysData[M]['LASER650']['target']=sysData[M]['LASER650']['default']
    sysData[M]['LASER650']['ON']=0
    
    FP='FP1'
    sysData[M][FP]['ON']=0
    sysData[M][FP]['LED']="LEDB"
    sysData[M][FP]['Base']=0
    sysData[M][FP]['Emit1']=0
    sysData[M][FP]['Emit2']=0
    sysData[M][FP]['BaseBand']="CLEAR"
    sysData[M][FP]['Emit1Band']="nm510"
    sysData[M][FP]['Emit2Band']="nm550"
    sysData[M][FP]['Gain']="x10"
    sysData[M][FP]['BaseRecord']=[]
    sysData[M][FP]['Emit1Record']=[]
    sysData[M][FP]['Emit2Record']=[]
    FP='FP2'
    sysData[M][FP]['ON']=0
    sysData[M][FP]['LED']="LEDD"
    sysData[M][FP]['Base']=0
    sysData[M][FP]['Emit1']=0
    sysData[M][FP]['Emit2']=0
    sysData[M][FP]['BaseBand']="CLEAR"
    sysData[M][FP]['Emit1Band']="nm583"
    sysData[M][FP]['Emit2Band']="nm620"
    sysData[M][FP]['BaseRecord']=[]
    sysData[M][FP]['Emit1Record']=[]
    sysData[M][FP]['Emit2Record']=[]
    sysData[M][FP]['Gain']="x10"
    FP='FP3'
    sysData[M][FP]['ON']=0
    sysData[M][FP]['LED']="LEDE"
    sysData[M][FP]['Base']=0
    sysData[M][FP]['Emit1']=0
    sysData[M][FP]['Emit2']=0
    sysData[M][FP]['BaseBand']="CLEAR"
    sysData[M][FP]['Emit1Band']="nm620"
    sysData[M][FP]['Emit2Band']="nm670"
    sysData[M][FP]['BaseRecord']=[]
    sysData[M][FP]['Emit1Record']=[]
    sysData[M][FP]['Emit2Record']=[]
    sysData[M][FP]['Gain']="x10"
 
    for PUMP in ['Pump1','Pump2','Pump3','Pump4']:
        sysData[M][PUMP]['default']=0.0;
        sysData[M][PUMP]['target']=sysData[M][PUMP]['default']
        sysData[M][PUMP]['ON']=0
        sysData[M][PUMP]['direction']=1.0
        sysDevices[M][PUMP]['threadCount']=0
        sysDevices[M][PUMP]['active']=0
    
    
    sysData[M]['Heat']['default']=0;
    sysData[M]['Heat']['target']=sysData[M]['Heat']['default']
    sysData[M]['Heat']['ON']=0

    sysData[M]['Thermostat']['default']=37.0;
    sysData[M]['Thermostat']['target']=sysData[M]['Thermostat']['default']
    sysData[M]['Thermostat']['ON']=0
    sysData[M]['Thermostat']['Integral']=0
    sysData[M]['Thermostat']['last']=-1

    sysData[M]['Stir']['target']=sysData[M]['Stir']['default']
    sysData[M]['Stir']['ON']=0
    
    sysData[M]['Light']['target']=sysData[M]['Light']['default']
    sysData[M]['Light']['ON']=0
    sysData[M]['Light']['Excite']='LEDD'
    
    sysData[M]['Custom']['Status']=sysData[M]['Custom']['default']
    sysData[M]['Custom']['ON']=0
    sysData[M]['Custom']['Program']='C1'
    
    sysData[M]['Custom']['param1']=0.0
    sysData[M]['Custom']['param2']=0.0
    sysData[M]['Custom']['param3']=0.0
    
    sysData[M]['OD']['current']=0.0
    sysData[M]['OD']['target']=sysData[M]['OD']['default'];
    sysData[M]['OD0']['target']=65000.0
    sysData[M]['OD0']['raw']=65000.0
    sysData[M]['OD']['device']='LASER650'
    #sysData[M]['OD']['device']='LEDA'
    
    #if (M=='M0'):
    #    sysData[M]['OD']['device']='LEDA'
    
    
    sysData[M]['Volume']['target']=20.0
    
    clearTerminal(M)
    addTerminal(M,'System Initialised')
  
    sysData[M]['Experiment']['ON']=0
    sysData[M]['Experiment']['cycles']=0
    sysData[M]['Experiment']['threadCount']=0
    sysData[M]['Experiment']['startTime']=' Waiting '
    sysData[M]['Experiment']['startTimeRaw']=0
    sysData[M]['OD']['ON']=0
    sysData[M]['OD']['Measuring']=0
    sysData[M]['OD']['Integral']=0.0
    sysData[M]['OD']['Integral2']=0.0
    sysData[M]['Zigzag']['ON']=0
    sysData[M]['Zigzag']['target']=0.0
    sysData[M]['Zigzag']['SwitchPoint']=0
    sysData[M]['GrowthRate']['current']=sysData[M]['GrowthRate']['default']

    sysDevices[M]['Thermostat']['threadCount']=0

    channels=['nm410','nm440','nm470','nm510','nm550','nm583','nm620', 'nm670','CLEAR','NIR','DARK','ExtGPIO', 'ExtINT' , 'FLICKER']
    for channel in channels:
        sysData[M]['AS7341']['channels'][channel]=0
        sysData[M]['AS7341']['spectrum'][channel]=0
    DACS=['ADC0', 'ADC1', 'ADC2', 'ADC3', 'ADC4', 'ADC5']
    for DAC in DACS:
        sysData[M]['AS7341']['current'][DAC]=0

    sysData[M]['ThermometerInternal']['current']=0.0
    sysData[M]['ThermometerExternal']['current']=0.0
    sysData[M]['ThermometerIR']['current']=0.0
 
    sysData[M]['time']['record']=[]
    sysData[M]['OD']['record']=[]
    sysData[M]['OD']['targetrecord']=[]
    sysData[M]['Pump1']['record']=[]
    sysData[M]['Pump2']['record']=[]
    sysData[M]['Pump3']['record']=[]
    sysData[M]['Pump4']['record']=[]
    sysData[M]['Heat']['record']=[]
    sysData[M]['Light']['record']=[]
    sysData[M]['ThermometerInternal']['record']=[]
    sysData[M]['ThermometerExternal']['record']=[]
    sysData[M]['ThermometerIR']['record']=[]
    sysData[M]['Thermostat']['record']=[]
    
    sysData[M]['GrowthRate']['record']=[]

    # Turn off device references for simulated script
    sysDevices[M]['ThermometerInternal']['device']=0 # <<<==================
    sysDevices[M]['ThermometerExternal']['device']=0 # <<<==================
    sysDevices[M]['DAC']['device']=0 # <<<==================
    sysDevices[M]['AS7341']['device']=0 # <<<==================
    sysDevices[M]['Pumps']['device']=0 # <<<==================
    sysDevices[M]['Pumps']['startup']=0 # <<<==================
    sysDevices[M]['Pumps']['frequency']=0x1e #200Hz PWM frequency
    sysDevices[M]['PWM']['device']=0 # <<<==================
    sysDevices[M]['PWM']['startup']=0
    sysDevices[M]['PWM']['frequency']=0x03# 0x14 = 300hz, 0x03 is 1526 Hz PWM frequency for fan/LEDs, maximum possible. Potentially dial this down if you are getting audible ringing in the device! 
    #There is a tradeoff between large frequencies which can make capacitors in the 6V power regulation oscillate audibly, and small frequencies which result in the number of LED "ON" cycles varying during measurements.
    sysDevices[M]['ThermometerIR']['device']=0 # <<<==================
    sysDevices[M]['ThermometerIR']['address']=0x5a 
 
    scanDevices(M)
    if(sysData[M]['present']==1):
        turnEverythingOff(M)
        print(str(datetime.now()) + " Initialised ", M)    # <<<==================

def initialiseAll():
    # Initialisation function which runs at when software is started for the first time.
    sysItems['Multiplexer']['device']=0 # <<<==================
    sysItems['FailCount']=0
    time.sleep(2.0) #This wait is to allow the watchdog circuit to boot.
    print(str(datetime.now()) + ' Initialising devices')

    for M in ['M0','M1','M2','M3','M4','M5','M6','M7']:
        initialise(M)
    scanDevices("all")

def scanDevices(which):
    #Scans to decide which devices are plugged in/on. Does this by trying to communicate with their internal thermometers (if this communication failes, software assumes device is not present)
    global sysData
    which=str(which)
    
    if which=="all":
        for M in ['M0','M1','M2','M3','M4','M5','M6','M7']:
            sysData[M]['present']=1
           # I2CCom(M,'ThermometerInternal',1,16,0x05,0,0) # <<<==================
            sysData[M]['DeviceID']=GetID(M)
    else: 
        
        sysData[which]['present']=1
      #  I2CCom(which,'ThermometerInternal',1,16,0x05,0,0) # <<<==================
        sysData[which]['DeviceID']=GetID(which)

    return ('', 204)

def GetID(M):
    #Gets the CHi.Bio reactor's ID, which is basically just the unique ID of the infrared thermometer.
    global sysData
    M=str(M)
    ID=''
    if sysData[M]['present']==1:
        pt1=0 # <<<==================
        pt2=0 # <<<==================
        pt3=0 # <<<==================
        pt4=0 # <<<==================
        ID = pt1+pt2+pt3+pt4
        
    return ID

def turnEverythingOff(M):
    # Function which turns off all actuation/hardware.
    for LED in ['LEDA','LEDB','LEDC','LEDD','LEDE','LEDF','LEDG']:
        sysData[M][LED]['ON']=0
        
    sysData[M]['LASER650']['ON']=0
    sysData[M]['Pump1']['ON']=0
    sysData[M]['Pump2']['ON']=0
    sysData[M]['Pump3']['ON']=0
    sysData[M]['Pump4']['ON']=0
    sysData[M]['Stir']['ON']=0
    sysData[M]['Heat']['ON']=0
    sysData[M]['UV']['ON']=0
    
    # I2CCom(M,'DAC',0,8,int('00000000',2),int('00000000',2),0)  # <<<==================
    #setPWM(M,'PWM',sysItems['All'],0,0)  # <<<==================
    #setPWM(M,'Pumps',sysItems['All'],0,0)  # <<<==================
    
    SetOutputOn(M,'Stir',0)
    SetOutputOn(M,'Thermostat',0)
    SetOutputOn(M,'Heat',0)
    SetOutputOn(M,'UV',0)
    SetOutputOn(M,'Pump1',0)
    SetOutputOn(M,'Pump2',0)
    SetOutputOn(M,'Pump3',0)
    SetOutputOn(M,'Pump4',0)


def addTerminal(M,strIn):
    #Responsible for adding a new line to the terminal in the UI.
    global sysData
    now=datetime.now()
    timeString=now.strftime("%Y-%m-%d %H:%M:%S ")
    sysData[M]['Terminal']['text']=timeString + ' - ' +  str(strIn) + '</br>' + sysData[M]['Terminal']['text']
    
def clearTerminal(M):
    #Deletes everything from the terminal.
    global sysData
    M=str(M)
    if (M=="0"):
        M=sysItems['UIDevice']
        
    sysData[M]['Terminal']['text']=''
    addTerminal(M,'Terminal Cleared')
    return ('', 204)   

def SetOutputOn(M,item,force):
    #General function used to switch an output on or off.
    global sysData
    item = str(item)
    
    force = int(force)
    M=str(M)
    if (M=="0"):
        M=sysItems['UIDevice']
    #The first statements are to force it on or off it the command is called in force mode (force implies it sets it to a given state, regardless of what it is currently in)
    if (force==1):
        sysData[M][item]['ON']=1
        SetOutput(M,item)
        return ('', 204)    
    
    elif(force==0):
        sysData[M][item]['ON']=0;
        SetOutput(M,item)
        return ('', 204)    
    
    #Elsewise this is doing a flip operation (i.e. changes to opposite state to that which it is currently in)
    if (sysData[M][item]['ON']==0):
        sysData[M][item]['ON']=1
        SetOutput(M,item)
        return ('', 204)    
    
    else:
        sysData[M][item]['ON']=0;
        SetOutput(M,item)
        return ('', 204)    


def SetOutput(M,item):
    #Here we actually do the digital communications required to set a given output. This function is called by SetOutputOn above as required.
    global sysData
    global sysItems
    global sysDevices
    M=str(M)
    #We go through each different item and set it going as appropriate.


######################################
# Custom programs
######################################

def SetCustom(Program,Status):
    #Turns a custom program on/off.
    
    global sysData
    M=sysItems['UIDevice']
    item="Custom"
    if sysData[M][item]['ON']==1:
        sysData[M][item]['ON']=0
    else:
        sysData[M][item]['Program']=str(Program)
        sysData[M][item]['Status']=float(Status)
        sysData[M][item]['ON']=1
        sysData[M][item]['param1']=0.0 #Thus parameters get reset each time you restart your program.
        sysData[M][item]['param2']=0.0
        sysData[M][item]['param3']=0.0
    return('',204)
        
        
def CustomProgram(M):
    #Runs a custom program, some examples are included. You can remove/edit this function as you see fit.
    #Note that the custom programs (as set up at present) use an external .csv file with input parameters. THis is done to allow these parameters to easily be varied on the fly. 
    global sysData
    M=str(M)
    program=sysData[M]['Custom']['Program']
    #Subsequent few lines reads in external parameters from a file if you are using any.

    
    if (program=="C1"): 
        print('\n')
        print('custom program:')
        print('hi')
        print("let's get OD")
        print(sysData[M]['OD']['current'])
        print("is this OD more than threshold?")
        answer = sysData[M]['OD']['current']>3.0
        
        if answer:
            print("yes, let's do something\n")
        else:
            print("no, keep going\n")
    
    elif (program=="C2"): 
        # measure OD
        MeasureOD(M)
    elif (program=="C3"): 
        # turn pumps on or off
        SetOutputOn(M,'Pump1',0)
        SetOutputOn(M,'Pump2',0)
        SetOutputOn(M,'Pump3',0)
        SetOutputOn(M,'Pump4',0)
    elif (program=="C4"): 
        pass
    elif (program=="C5"): 
        pass
    elif (program=="C6"):
        pass
                
                
    return

######################################
# Experiment functions
######################################

# @application.route("/Experiment/<value>/<M>",methods=['POST'])  <<< Start with frontpanel button
def ExperimentStartStop(M,value):
    #Stops or starts an experiment. 
    global sysData
    global sysDevices
    global sysItems
    M=str(M)
    if (M=="0"):
        M=sysItems['UIDevice']
       
    value=int(value)
    #Turning it on involves keeping current pump directions,
    if (value and (sysData[M]['Experiment']['ON']==0)):
        sysData[M]['Experiment']['ON']=1
        addTerminal(M,'Experiment Started')

        if (sysData[M]['Experiment']['cycles']==0):
            now=datetime.now()
            timeString=now.strftime("%Y-%m-%d %H:%M:%S")
            sysData[M]['Experiment']['startTime']=timeString
            sysData[M]['Experiment']['startTimeRaw']=now
        
        sysData[M]['Pump1']['direction']=1.0 #Sets pumps to go forward.
        sysData[M]['Pump2']['direction']=1.0

        turnEverythingOff(M)
        
        SetOutputOn(M,'Thermostat',1)

        # start experiment loop here
        sysDevices[M]['Experiment']=Thread(target = runExperiment, args=(M,'placeholder'))
 #       sysDevices[M]['Experiment'].setDaemon(True)
        sysDevices[M]['Experiment'].start();
        
    else:
        sysData[M]['Experiment']['ON']=0
        sysData[M]['OD']['ON']=0
        addTerminal(M,'Experiment Stopping at end of cycle')
        SetOutputOn(M,'Pump1',0)
        SetOutputOn(M,'Pump2',0)
        SetOutputOn(M,'Stir',0)
        SetOutputOn(M,'Thermostat',0)
        
    return ('', 204)

def runExperiment(M,placeholder):
    #Primary function for running an automated experiment.
    M=str(M)
   
    global sysData
    global sysItems
    global sysDevices
    
    sysData[M]['Experiment']['threadCount']=(sysData[M]['Experiment']['threadCount']+1)%100
    currentThread=sysData[M]['Experiment']['threadCount']
    print('new thread', currentThread)

    # Get time running in seconds
    now=datetime.now()
    elapsedTime=now-sysData[M]['Experiment']['startTimeRaw']
    elapsedTimeSeconds=round(elapsedTime.total_seconds(),2)
    sysData[M]['Experiment']['cycles']=sysData[M]['Experiment']['cycles']+1
    addTerminal(M,'Cycle ' + str(sysData[M]['Experiment']['cycles']) + ' Started')
    CycleTime=sysData[M]['Experiment']['cycleTime']

    SetOutputOn(M,'Stir',0) #Turning stirring off
    print('stirring off')
#    time.sleep(5.0) #Wait for liquid to settle.

    # CHECK IF USER HAS STOPPED EXPT FROM FRONT PANEL
    if (sysData[M]['Experiment']['ON']==0):
        print('stopping')
        turnEverythingOff(M)
        sysData[M]['Experiment']['cycles']=sysData[M]['Experiment']['cycles']-1 # Cycle didn't finish, don't count it.
        addTerminal(M,'Experiment Stopped')
        return
    
    sysData[M]['OD']['Measuring']=1 #Begin measuring - this flag is just to indicate that a measurement is currently being taken.

    #We now meausre OD 4 times and take the average to reduce noise when in auto mode!
    ODV=0.0
    print('measuring OD')
    for i in [0, 1, 2, 3]:
        ODV=1.0+currentThread
 #       time.sleep(0.25)
    sysData[M]['OD']['current']=ODV/4.0
    
    print('measure temps and FP')
#   MeasureTemp(M,'Internal') #Measuring all temperatures
#    MeasureTemp(M,'External')
#    MeasureTemp(M,'IR')
#    MeasureFP(M) #And now fluorescent protein concentrations. 
 
    # CHECK IF USER HAS STOPPED EXPT FROM FRONT PANEL   
    if (sysData[M]['Experiment']['ON']==0): #We do another check post-measurement to see whether we need to end the experiment.
        turnEverythingOff(M)
        sysData[M]['Experiment']['cycles']=sysData[M]['Experiment']['cycles']-1 # Cycle didn't finish, don't count it.
        addTerminal(M,'Experiment Stopped')
        return


    sysData[M]['OD']['Measuring']=0
    print('measurements finished')
    if (sysData[M]['OD']['ON']==1):
        print('regulating OD')
        RegulateOD(M) #Function that calculates new target pump rates, and sets pumps to desired rates. 
    
    print('light actuation on')
 #   LightActuation(M,1) 
    
    if (sysData[M]['Custom']['ON']==1): #Check if we have enabled custom programs
        CustomThread=Thread(target = CustomProgram, args=(M,)) #We run this in a thread in case we are doing something slow, we dont want to hang up the main l00p. The comma after M is to cast the args as a tuple to prevent it iterating over the thread M
        CustomThread.setDaemon(True)
        CustomThread.start();

    
#    Pump2Ontime=sysData[M]['Experiment']['cycleTime']*1.05*abs(sysData[M]['Pump2']['target'])*sysData[M]['Pump2']['ON']+0.5 #The amount of time Pump2 is going to be on for following RegulateOD above.
#    time.sleep(Pump2Ontime) #Pause here is to prevent output pumping happening at the same time as stirring.
    
    print('stirring on')
    SetOutputOn(M,'Stir',1) #Start stirring again.

    if(sysData[M]['Experiment']['cycles']%10==9): #Dont want terminal getting unruly, so clear it each 10 rotations.
        clearTerminal(M)
    
    #######Below stores all the results for plotting later
    print('record data')

# CHECK IF USER HAS STOPPED EXPT FROM FRONT PANEL
    if (sysData[M]['Experiment']['ON']==0):
        turnEverythingOff(M)
        addTerminal(M,'Experiment Stopped')
        return
    
    nowend=datetime.now()
    elapsedTime2=nowend-now
    elapsedTimeSeconds2=round(elapsedTime2.total_seconds(),2)
    sleeptime=CycleTime-elapsedTimeSeconds2
    if (sleeptime<0):
        sleeptime=0
        addTerminal(M,'Experiment Cycle Time is too short!!!')    
        
 #   time.sleep(sleeptime)
    print('light actuation off')
 #   LightActuation(M,0) #Turn light actuation off if it is running.
    addTerminal(M,'Cycle ' + str(sysData[M]['Experiment']['cycles']) + ' Complete')

    print(sysData[M]['Experiment']['ON'])
    print(sysData[M]['Experiment']['threadCount'])
    print(currentThread)
    print('pausing\n')
    time.sleep(1.0)
    #Now we run this function again if the automated experiment is still going.
    if (sysData[M]['Experiment']['ON'] and sysData[M]['Experiment']['threadCount']==currentThread):
        sysDevices[M]['Experiment']=Thread(target = runExperiment, args=(M,'placeholder'))
   #     sysDevices[M]['Experiment'].setDaemon(True)
        sysDevices[M]['Experiment'].start();
        
    else: 
        turnEverythingOff(M)
 #       print('stopping')
        addTerminal(M,'Experiment Stopped')


if __name__ == '__main__':
    initialiseAll()
    sysData['M0']['Experiment']['ON']=0
    sysData['M0']['Custom']['ON']=1
    sysData['M0']['Custom']['Program']='C1'
    ExperimentStartStop(0,1)

