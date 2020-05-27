#!/usr/bin/python2.7
# -*- coding:utf-8 -*-

######################################################################
#
#  Application Tactile pour le CJB
#  Auteur : Simon Maulini
#  Début : 07.01.2014
#
######################################################################

#from kivy.app
from kivy.app import App

#from kivy.properties
from kivy.properties import ObjectProperty
from kivy.properties import NumericProperty
from kivy.properties import StringProperty

#from kivy.graphics
from kivy.graphics import Rectangle

#from kivy uix
from kivy.uix.widget import Widget
from kivy.uix.carousel import Carousel
from kivy.uix.image import Image
from kivy.uix.scatter import Scatter
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

#Standard moduls
from random import randint
import os
import sqlite3 as sql

class WorkFlow(Widget):
	#btnSelect = ObjectProperty(0)
	selectCategorie = ObjectProperty(0)
	car = ObjectProperty(0)

class ImgCarousel(Image):
	pass

######################################################################
#  Class MyCarousel héritée de Carousel => kivy.uix.carousel
######################################################################
class MyCarousel(Carousel):
	categories = []

	def __init__(self,**kwargs):
		super(MyCarousel,self).__init__(**kwargs)

		c = sql.connect('database/table.db')
		cur = c.cursor()

		cur.execute('SELECT imgCategorie, idCategorie, labelCategorie FROM categories')
		data = cur.fetchall()

		for cat in data:
			filename = 'img/carousel/' + cat[0]
			img = ImgCarousel(source=filename,allow_stretch=True)

			self.add_widget(img)
			catData = {}
			catData["id"] = cat[1]
			catData["label"] = cat[2]
			self.categories.append(catData)

		cur.close()
		c.close()

# End of MyCarousel

########################################################################
# Class MyScatter héritée de Scatter => kivy.uix.scatter
########################################################################
class MyScatter(Scatter):
	source = StringProperty('')
	btn = Button()
	id = NumericProperty(0)
	description = StringProperty('')

# End of MyScatter

#########################################################################
# Class ButtonInfo héritée de Widget => kivy.uix.widget
#########################################################################
class ButtonInfo(Widget):
	descriptionImg = StringProperty('')

	def on_touch_down(self,touch):
		if self.collide_point(*touch.pos):
			self.displayInfo()

	def displayInfo(self):
		btnClose = Button(text='Fermer',size_hint_y=None, height=50)
		content = BoxLayout(orientation='vertical')
		content.add_widget(Label(text=self.descriptionImg))
		content.add_widget(btnClose)
		popup = Popup(content=content,title='Description', size_hint=(None,None), size=(600,400), auto_dismiss=False)
		btnClose.bind(on_release=popup.dismiss)
		popup.open()

# End of ButtonInfo

#######################################################################
#  Class VirtualDesktop heritée de Widget => kivy.uix.widget
#######################################################################
class VirtualDesktop(Widget):
	btnReturn = ObjectProperty(0)
	categorie = NumericProperty(0)
	scatters = []

	def __init__(self,**kwargs):
		super(VirtualDesktop,self).__init__(**kwargs)

                for s in self.scatters:
                        self.remove_widget(s)

                self.scatters = []

                c = sql.connect('database/table.db')
                cur = c.cursor()

                cur.execute('SELECT imgElement, idElement, description FROM elements WHERE idCategorie = ' + str(self.categorie))
                data = cur.fetchall()

                x = 100
                y = 100
                for elmt in data:
                        filename = 'img/desktop/' + elmt[0]

                        x += 50
                        y += 50

                        sc = MyScatter(source=filename,pos=(x,y))
                        sc.id = elmt[1]
                        sc.description = elmt[2]

                        self.scatters.append(sc)
                        self.add_widget(sc)

                cur.close()
                c.close()

# End of VirtualDesktop

class TactilEnv(Widget):
	workFlow = ObjectProperty(0)
	virtualDesktops = {}

	def __init__(self,**kwargs):
		super(TactilEnv,self).__init__(**kwargs)

		#self.remove_widget(self.virtualDesktop)

		#Association des event
		self.workFlow.selectCategorie.bind(on_release=self.selectImg)

	def selectImg(self,obj):
		cat = self.workFlow.car.categories[self.workFlow.car.index]['id']

		self.remove_widget(self.workFlow)

		if cat not in self.virtualDesktops.keys():
			vd = VirtualDesktop(size=self.size,categorie=cat)
			vd.btnReturn.bind(on_release=self.returnToCat)
			self.virtualDesktops[cat] = vd

		self.add_widget(self.virtualDesktops[cat])
		
		#self.add_widget(self.virtualDesktop)
		#self.virtualDesktop.chargeImg(cat)
		#self.virtualDesktop.btnReturn.bind(on_release=self.returnToCat)

	def returnToCat(self,obj):
		self.clear_widgets()
		self.add_widget(self.workFlow)


class TactilApp(App):
	def build(self):
		tactil = TactilEnv()
		return tactil

#######################################################################
# Main programm
#######################################################################
if __name__ == '__main__':
	TactilApp().run()
