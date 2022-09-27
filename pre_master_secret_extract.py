
import asyncio, sys, re;

async def pre_master_secret_extract_worker(async_task_queue):
    while True:
        line = await async_task_queue.get();
        
        if re.search(r".*f5ethtrailer.tls.keylog.*\"(.*)\"", line, re.I):
            with open("pre_master_secret.key", "a") as file:
                file.write(re.search(r".*f5ethtrailer.tls.keylog.*\"(.*)\"", line, re.I)[1] + "\n");
            
        async_task_queue.task_done();
    
async def main():
    async_task_queue = asyncio.Queue();
    
    with open(sys.argv[1], "r") as file:
        for line in file.read().split("\n"):
            await async_task_queue.put(line);
            
    for _ in range(10000):
        asyncio.Task(pre_master_secret_extract_worker(async_task_queue));
        
    await async_task_queue.join();
    
if "__main__" in __name__:
    if len (sys.argv[1:]) != 1:
        print(f"\n[+] Usage: Python3 {sys.argv[0]} Wireshark_Dissection_Json_File\n");
    else:
        asyncio.run(main());
        