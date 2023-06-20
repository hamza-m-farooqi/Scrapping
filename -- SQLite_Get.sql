-- SQLite
-- SELECT id, date, platform_id, page_number, image_number, image_id, image_name, image_src, image_promt, image_download_status
-- FROM AI_Generated_Images_Scrapping_Info
-- WHERE platform_id=2
-- ORDER BY image_number DESC;



-- DELETE FROM AI_Generated_Images_Scrapping_Info WHERE platform_id=2 and page_number=197


SELECT * FROM AI_Generated_Images_Scrapping_Info
WHERE platform_id=3