##
import asyncio
import json
import nest_asyncio
from aiohttp import ClientSession
import requests

from Code import z_ns as ns
from Code import z_cf as cf


nest_asyncio.apply()  # Run this line in cell mode to code work

dirs = ns.Dirs()
rq = ns.ReqParams()

ScN = 'b'
PgsPn = dirs.raw / "pgs.txt"


async def download_page_json(params):
    async with ClientSession() as session:
        async with session.get(rq.search_url,
                               verify_ssl=False,
                               params=params) as resp:
            content = await resp.json()
            print(f"Finished downloading")
            return content


async def write_to_json(content, file_pn):
    with open(file_pn, "w") as f:
        json.dump(content, f)
    print(f'saved as {file_pn}')


async def web_scrape_task(param, file_pn):
    content = await download_page_json(param)
    await write_to_json(content, file_pn)


async def pages_reading_main(all_params, all_file_pns):
    tasks = []
    for u, f in zip(all_params, all_file_pns):
        tasks.append(web_scrape_task(u, f))
    await asyncio.wait(tasks)


def main():
    pass
    ##
    assert cf.is_machine_connected_to_internet()
    ##
    if PgsPn.exists():
        with open(PgsPn, "r") as f:
            pgscraped = int(f.read())
    else:
        pgscraped = 0
    print(f'{pgscraped} pages has been crawled before!')
    ##
    first_page_response = requests.get(rq.search_url,
                                       verify=False,
                                       params=rq.params)
    print(first_page_response)
    assert first_page_response.status_code == 200
    ##
    frst_page_data = first_page_response.json()
    print(frst_page_data)
    ##
    total_pages = frst_page_data["Page"]
    print(f'Total pages are {total_pages}')
    ##
    pages_2crawl = total_pages - pgscraped + 1
    print(f'I am going to scrape first {pages_2crawl} pages, which are new!')
    ##
    all_params_2crawl = []
    all_fpns = []
    for page_num in range(1, pages_2crawl + 1):
        page_reqparam = rq.params.copy()
        page_reqparam['PageNumber'] = page_num
        all_params_2crawl.append(page_reqparam)
        all_fpns.append(dirs.jsons / f"{page_num}.json")
    print(all_params_2crawl[-1])
    ##
    clusters = cf.return_clusters_indices(all_params_2crawl)
    ##
    for i in range(len(clusters) - 1):
        start_index = clusters[i]
        end_index = clusters[i + 1]
        print(f'{start_index} to {end_index}')

        params = all_params_2crawl[start_index: end_index]
        fpns = all_fpns[start_index: end_index]

        asyncio.run(pages_reading_main(params, fpns))
    ##
    with open(PgsPn, 'w') as f:
        f.write(str(total_pages))
        print(total_pages)


##
if __name__ == "__main__":
    main()
    print(f'{ScN}.py Done!')
else:
    pass
    ##
