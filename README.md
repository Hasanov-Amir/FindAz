# FindAz API
## Endpoints

### 1. Method GET, POST
    /api/items
#### Response GET:
    {
        "items": [
            {"_id": ObjectId(...), ...},
            {"_id": ObjectId(...), ...},
            ...
        ]
    }
#### Response POST:
    {
        "item_id": ObjectId(...)
    }
### 2. Method GET
    /api/items/<string:item_id>
#### Response GET:
    {
        "item": {
            "_id": ObjectId(...),
            ...
        }
    }
### 3. Method PATCH
    /api/items/add-photo/<string:item_id>
#### Response PATCH:
    {
        "image0_url": "...",
        "main_file_url": "..."
    }
### 4. Method GET
    /<string:file>
#### Response GET:
    // file...
