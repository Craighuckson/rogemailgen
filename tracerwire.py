#demo for tracer wire email

from data import Email
from pathlib import Path
import easygui as eg

#get filename
xl = eg.fileopenbox(msg='Please select excel file',default='*.xlsx')
pic = eg.fileopenbox(msg='Please select screenshot',default='*.png')

#remove unnecessary file info from filename
x1 = Path(xl)
xl = x1.stem + x1.suffix

p1 = Path(pic)
pic = p1.stem + p1.suffix

#get ticket number and address
vals = eg.multenterbox(msg='Please enter ticket number and address',
                       title='Enter values',
                       fields=['Ticket number: ','Address: ']
                       )


Email.write_tracer_wire(Email.tolist,Email.cclist,vals[0],vals[1],xl,pic)
                    
                        
