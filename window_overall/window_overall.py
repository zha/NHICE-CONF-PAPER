import pywincalc

class WinProp():
    __slot__ = ('_system_wdith', '_system_height',  '_overallSHGC', '_overallU')
    def __init__(self, system_width, system_height,  glz_out_dir, glz_in_dir, gap):
        self._system_width = system_width
        self._system_height = system_height
        self._overallU, self._overallSHGC = self.__overallCalc(system_width, system_height,  
                                                    glz_out_dir, glz_in_dir, self.__convert(gap))

    
    @property
    def system_width(self):
        return self._system_width
    @property
    def system_height(self):
        return self._system_height
    @property
    def overallU(self):
        return self._overallU

    @property
    def overallSHGC(self):
        return self._overallSHGC


    @staticmethod
    def __overallCalc(system_width, system_height, glaze_1_dir, glaze_2_dir, gap_1):
        glaze_1 = pywincalc.parse_optics_file(glaze_1_dir)
        glaze_2 = pywincalc.parse_optics_file(glaze_2_dir)
        system_area = system_width * system_height

        frame_wdith  = 53e-3  # value taken from ASHRAE fundamentals for Aluminum with thermal break. For operable window
        

        glazing_width  = system_width - frame_wdith * 2
        glazing_height = system_height - frame_wdith * 2

        frame_area = system_area - glazing_width * glazing_height


        edge_width = 65e-3  # value taken from ASHRAE fundamentals, Section Edge-of-glass U-factor

        glazing_center_area = (glazing_width - edge_width * 2) * (glazing_height - edge_width * 2)
        glazing_edge_area = glazing_width * glazing_height - glazing_center_area




        standard_path = r"C:\Program Files (x86)\LBNL\LBNL Shared\Standards\W5_NFRC_2003.std" 
        standard = pywincalc.load_standard(standard_path)


        gaps = [gap_1]
        solid_layers = [glaze_1,glaze_2]

        glazing_system_tripple_layer = pywincalc.Glazing_System(solid_layers, gaps, standard, system_width, system_height)
        center_u = glazing_system_tripple_layer.u().result
        glazing_SHGC = glazing_system_tripple_layer.shgc().result
        edge_u = (0.078+ 0.998 * (center_u/5.678263) -0.175*(center_u/5.678263) **2)*5.678263
        frame_u = 5.22   # ASHRAE Fundamentals
        overall_u = (center_u * glazing_center_area + frame_u * frame_area + edge_u * glazing_edge_area)/system_area

    #     SHGC_frame = 0.9*frame_u/26
        frame_absrptivity = 0.7    # value taken from Calculating the Solar Heat Gain of Window Frames 
        
        hi = 8 + 4 * 5.67e-8 * 0.8 * (30 + 273.15)**3   # These are the summer conditions used in ISO 15099, formula ffrom ASHREA fundamentals, emissivity taken from Heat and Mass textbook for anodized aluminum
        SHGC_frame = frame_absrptivity * 0.49 * frame_u / hi  # Formula from ASHRAE Fundamental 

        SHGC_overall = (SHGC_frame * frame_area + glazing_SHGC * (glazing_width * glazing_height))/system_area  # formula from ASHRAE fundamentals
        return overall_u, SHGC_overall

    @staticmethod
    def __convert(gap):
        assert isinstance(gap, str)
        if str.lower(gap) == 'air':
            return pywincalc.Gap_Data(pywincalc.Gas_Type.AIR, .0127)
