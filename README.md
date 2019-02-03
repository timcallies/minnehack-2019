# TEAM BIG BRAIN 
  
## SUSTAINABLITIY SCANNER
  
### TABLE 41
  
#### Tyler Beverley, Tim Callies, Andrew Bates
  

We devoloped a program that allows consusmers to scan UPC barcodes to get some information about that product, such as where that product is from, where the product can be found locally nearby, and how much C02 was created durring the shipping of this product. We hope this product will help promote sustainable argicltural practices (such as growing locally to avoid creating C02 durring shipping), and we hope that this product will strengthen local argicultural communites. 


### How it works
1. We first had to obtain a UPC barcode from the user, we did this using HTML so that the interface was mobile friendly. 
2. We needed to adjust the image so that we could get an accurate reading from the barcode image. Although more could be done in this regard
3. After we had the UPC number, we could then hit the barcode lookup API to give us info about who the manufactor is, what the ingrediants are, and the nutritiional facts for the product.  
4. Once we had that information, we got GPS coords from the user, and GPS coords for where the product came from. So that we could calculate the distance between the two. 
5. Once we had the distance between the two we could estimate the amount of C02 that was created in order to ship the product. 
6. Since we also had the user's location we could recomend a local farm for the user to get that kind of product from. 
