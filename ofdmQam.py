#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Ofdmqam
# Generated: Tue Jun  6 21:05:14 2017
##################################################

from gnuradio import analog
from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import wxgui
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from gnuradio.wxgui import fftsink2
from gnuradio.wxgui import forms
from grc_gnuradio import blks2 as grc_blks2
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import wx

class ofdmQam(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="Ofdmqam")
        _icon_path = "/usr/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
        self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 32000
        self.ampNoise = ampNoise = 0

        ##################################################
        # Blocks
        ##################################################
        _ampNoise_sizer = wx.BoxSizer(wx.VERTICAL)
        self._ampNoise_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_ampNoise_sizer,
        	value=self.ampNoise,
        	callback=self.set_ampNoise,
        	label='ampNoise',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._ampNoise_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_ampNoise_sizer,
        	value=self.ampNoise,
        	callback=self.set_ampNoise,
        	minimum=0,
        	maximum=100,
        	num_steps=1,
        	style=wx.SL_VERTICAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_ampNoise_sizer)
        self.wxgui_fftsink2_0 = fftsink2.fft_sink_c(
        	self.GetWin(),
        	baseband_freq=0,
        	y_per_div=10,
        	y_divs=10,
        	ref_level=0,
        	ref_scale=2.0,
        	sample_rate=samp_rate,
        	fft_size=1024,
        	fft_rate=15,
        	average=False,
        	avg_alpha=None,
        	title="FFT Transmissao",
        	peak_hold=False,
        )
        self.GridAdd(self.wxgui_fftsink2_0.win, 1, 1, 1, 1)
        self.digital_ofdm_mod_0 = grc_blks2.packet_mod_f(digital.ofdm_mod(
        		options=grc_blks2.options(
        			modulation="bpsk",
        			fft_length=64,
        			occupied_tones=52,
        			cp_length=16,
        			pad_for_usrp=True,
        			log=None,
        			verbose=None,
        		),
        	),
        	payload_length=0,
        )
        self.digital_ofdm_demod_0 = grc_blks2.packet_demod_f(digital.ofdm_demod(
        		options=grc_blks2.options(
        			modulation="bpsk",
        			fft_length=64,
        			occupied_tones=52,
        			cp_length=16,
        			snr=10,
        			log=None,
        			verbose=None,
        		),
        		callback=lambda ok, payload: self.digital_ofdm_demod_0.recv_pkt(ok, payload),
        	),
        )
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_float*1, "/home/luan/Documentos/GNU/ofdmQamLuan_TxRx_File/lena_Tx.jpeg", True)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_float*1, "/home/luan/Documentos/GNU/ofdmQamLuan_TxRx_File/lena_Rx.jpeg", False)
        self.blocks_file_sink_0.set_unbuffered(False)
        self.blocks_add_xx_0 = blocks.add_vcc(1)
        self.analog_noise_source_x_0 = analog.noise_source_c(analog.GR_GAUSSIAN, ampNoise, 0)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.digital_ofdm_mod_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.wxgui_fftsink2_0, 0))
        self.connect((self.analog_noise_source_x_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.blocks_file_source_0, 0), (self.digital_ofdm_mod_0, 0))
        self.connect((self.digital_ofdm_demod_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.digital_ofdm_demod_0, 0))


# QT sink close method reimplementation

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.wxgui_fftsink2_0.set_sample_rate(self.samp_rate)
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)

    def get_ampNoise(self):
        return self.ampNoise

    def set_ampNoise(self, ampNoise):
        self.ampNoise = ampNoise
        self.analog_noise_source_x_0.set_amplitude(self.ampNoise)
        self._ampNoise_slider.set_value(self.ampNoise)
        self._ampNoise_text_box.set_value(self.ampNoise)

if __name__ == '__main__':
    import ctypes
    import os
    if os.name == 'posix':
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    (options, args) = parser.parse_args()
    tb = ofdmQam()
    tb.Start(True)
    tb.Wait()

