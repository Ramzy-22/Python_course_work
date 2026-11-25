import hashlib
import json

def split_into_chunks(data, chunk_size):
    if chunk_size <= 0:
        raise ValueError("Invalid chunk size")
    result = []
    for i in range(0,len(data),chunk_size):
        result.append(data[i: i+chunk_size])
    return result

def calculate_cid(chunk):
    return hashlib.sha256(chunk).hexdigest()
    

def calculate_cids(chunks):
    results = []
    for chunk in chunks:
        cid = calculate_cid(chunk)
        results.append(cid)
    return results

def create_manifest(cids):
    manifest = {
        "chunks": cids
    }
    json_string = json.dumps(manifest)
    json_bytes = json_string.encode("utf-8")
    return json_bytes

def store_chunks(chunks):
    blocks = {}
    
    for chunk in chunks:
        val = calculate_cid(chunk)
        blocks[val] = chunk

    return blocks

def retrieve_chunks(cids, blocks):
    result = []
    for cid in cids:
        result.append(blocks[cid])
    return result

def reconstruct_file(cids, blocks):
    vals = retrieve_chunks(cids,blocks)
    result = b"".join(vals)
    return result
    
def reconstruct_from_manifest(manifest_bytes, blocks):
    manifest = json.loads(manifest_bytes)
    cids = manifest['chunks']
    return reconstruct_file(cids,blocks)

def save_block(cid, chunk):
    filename = f"storage/blocks/{cid}"
    with open(filename, "wb") as file:
        file.write(chunk)
cid = calculate_cid(b"ABCD")
save_block(cid, b"ABCD")

def load_block(cid):
    filename = f"storage/blocks/{cid}"
    with open(filename, 'rb') as file:
        data = file.read()
    return data

def save_manifest(cid, manifest_bytes):
    filename = f"storage/manifests/{cid}"
    with open(filename,'wb') as file:
        file.write(manifest_bytes)

def load_manifest(cid):
    filename = f"storage/manifests/{cid}"
    with open(filename, 'rb') as file:
        data = file.read()
    return data

def reconstruct_from_disk(manifest_cid):
    results = []
    manifest = json.loads(load_manifest(manifest_cid))
    cids = manifest["chunks"]
    for cid in cids:
        results.append(load_block(cid))
    data = b"".join(results)
    return data

manifest_cid = "1d1654691be42aba716e0a853aca4a263cde34544cfe838e28db42327db0ab83"

reconstructed = reconstruct_from_disk(manifest_cid)

print("Recovered data:", reconstructed)
print("Match:", reconstructed == b"ABCDEFGHIJ")

"""# 1. Original data
original = b"ABCDEFGHIJ"

# 2. Split data into chunks
chunks = split_into_chunks(original, 4)

# 3. Calculate CIDs for all chunks
cids = calculate_cids(chunks)

# 4. Save each chunk to disk
for cid, chunk in zip(cids, chunks):
    save_block(cid, chunk)

# 5. Create the manifest
manifest_bytes = create_manifest(cids)

# 6. Calculate the manifest CID
manifest_cid = calculate_cid(manifest_bytes)

# 7. Save the manifest to disk
save_manifest(manifest_cid, manifest_bytes)

# 8. Reconstruct the file from disk
reconstructed = reconstruct_from_disk(manifest_cid)

# 9. Compare the original and reconstructed data
print("Original:", original)
print("Manifest CID:", manifest_cid)
print("Reconstructed:", reconstructed)
print("Match:", original == reconstructed)"""