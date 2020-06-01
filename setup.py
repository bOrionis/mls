from distutils.core import setup

#with open("README.md", "r") as fh:
#    long_description = fh.read()

setup(
  name = 'ml_scanner',         
  packages = ['ml_scanner','ml_scanner/getDataML','ml_scanner/GUI','ml_scanner/saveData'],  
  version = '0.1.3',     
  license='MIT',       
  description = 'Scanner of ML publications',
  #long_description = long_description ,
  #long_description_content_type='text/markdown',
  author = 'Aldebaran bO',  
  author_email = '19.beta.Orionis@gmail.com',   
  url = 'https://github.com/bOrionis/mls/tree/saveData',  
  download_url = 'https://github.com/bOrionis/mls/tree/saveData', 
  keywords = ['Scrapper', 'Mercado libre', 'scanner', 'Monitoring'],  
  install_requires=[        
          'request',
          'PySimpleGUI'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha', 
    'Intended Audience :: End Users/Desktop',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3',    
  ],
)

