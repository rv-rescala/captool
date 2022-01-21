
for text in abema_list      abema_top       cmoa_list       cmoa_top        comick_list     comick_top      ebook_list      ebook_top       unext_list      unext_top comick_list_desktop unext_list_desktop; do
  echo $text 
  python captool/main.py $text ./conf ./dataset
done

