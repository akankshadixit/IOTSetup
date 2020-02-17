pragma solidity ^0.5.11;

contract IoTSmartContacrt{
    struct Resource{
        bytes32[] authorizedDevice;
    }
    struct Device{
        address owner;
        bytes32 deviceKey;
        uint numResources;
        bytes32[] resourceList;
        mapping(bytes32 => Resource) resourceStruct;
    }
     struct Manager{
        string name;
        bytes32[] deviceKeyList;
        mapping(bytes32 => Device) deviceStruct;
    }

    bytes32[] managerKeyList;
    mapping(bytes32 => Manager) managerStruct;

    event ManagerCreated(bytes32 _managerKey, string name);
    event DeviceCreated(bytes32 _managerKey, bytes32 _deviceKey, address indexed owner);
    //adds the manager to manager list and creates a mapping data structure correspoding to each manager
    function RegisterManager(string memory _name, bytes32 _managerKey)public returns(bool success){
        managerStruct[_managerKey].name = _name;
        managerKeyList.push(_managerKey);
        emit ManagerCreated(_managerKey, _name);
        return true;
    }

    //returns the number of managers registered
    function GetManagerCount()public view returns(uint managerCount){
        managerCount = managerKeyList.length;
        return managerCount;
    }
    //returns the number of devices registered with each manager
    function GetDeviceCountofManager(bytes32 _managerKey) public view returns(string memory name, uint deviceCount){
        return(managerStruct[_managerKey].name, managerStruct[_managerKey].deviceKeyList.length);
    }
    //returns the list of devicekeys registered with a particular manager corresponding to the managerKey
    function GetDeviceListofManager(bytes32 _managerKey) public view returns(bytes32[] memory){
        uint deviceCount = managerStruct[_managerKey].deviceKeyList.length;
        bytes32[] memory ret = new bytes32[](deviceCount);
        for(uint i = 0; i < deviceCount; i++){
            ret[i] = managerStruct[_managerKey].deviceKeyList[i];
        }
        return ret;
    }
    //managers sends a transaction to the blockchain everytime it wants to register a device under itself
    function RegisterDevicetoManager(bytes32 _managerKey, bytes32 _deviceKey) public returns(bool success){
        managerStruct[_managerKey].deviceKeyList.push(_deviceKey);
        managerStruct[_managerKey].deviceStruct[_deviceKey].owner = msg.sender;
        managerStruct[_managerKey].deviceStruct[_deviceKey].deviceKey = _deviceKey;
        emit DeviceCreated(_managerKey, _deviceKey, msg.sender);
        return true;
    }

     function AddResourcesforDevice(bytes32 _managerKey, bytes32 _deviceKey, bytes32[] memory _resourceList)public returns(bool success){
        uint resourceCount = _resourceList.length;
        for(uint i = 0; i < resourceCount; i++){
            managerStruct[_managerKey].deviceStruct[_deviceKey].numResources++;
            managerStruct[_managerKey].deviceStruct[_deviceKey].resourceList.push(_resourceList[i]);
        }
        return true;
    }
    //functiont to add a permission for a device s1 to access resource r of device s2
    function AddAccessControl(bytes32 _managerKey, bytes32 _permissionTo, bytes32 _permissionFrom, bytes32 _resourceName)public{
        managerStruct[_managerKey].deviceStruct[_permissionFrom].resourceStruct[_resourceName].authorizedDevice.push(_permissionTo);
    }
    //function to remove permission for a device s1 for a resource r of device s2
    function RevokePermission(bytes32 _managerKey, bytes32 _permissionTo, bytes32 _permissionFrom, bytes32 _resourceName)public
    returns(bytes32 deviceToBeRemoved){
        uint deviceCount = managerStruct[_managerKey].deviceStruct[_permissionFrom].resourceStruct[_resourceName].authorizedDevice.length;
        uint index;
        for(uint i = 0; i < deviceCount; i++){
           if(_permissionTo == managerStruct[_managerKey].deviceStruct[_permissionFrom].resourceStruct[_resourceName].authorizedDevice[i])
               index = i;
        }
        deviceToBeRemoved = managerStruct[_managerKey].deviceStruct[_permissionFrom].resourceStruct[_resourceName].authorizedDevice[index];
        managerStruct[_managerKey].deviceStruct[_permissionFrom].resourceStruct[_resourceName].authorizedDevice[index]
          =managerStruct[_managerKey].deviceStruct[_permissionFrom].resourceStruct[_resourceName].authorizedDevice[deviceCount-1];//last device replaced
        delete(managerStruct[_managerKey].deviceStruct[_permissionFrom].resourceStruct[_resourceName].authorizedDevice[deviceCount-1]);
        managerStruct[_managerKey].deviceStruct[_permissionFrom].resourceStruct[_resourceName].authorizedDevice.length--;
    }

    function RemoveDevicefromManager(bytes32 _managerKey, bytes32 _deviceKey)public payable returns(bytes32 deviceToBeRemoved){
        uint deviceCount = managerStruct[_managerKey].deviceKeyList.length;
        uint index;
        for(uint i = 0; i < deviceCount; i++){
           if(_deviceKey == managerStruct[_managerKey].deviceKeyList[i])
               index = i;
        }
        deviceToBeRemoved = managerStruct[_managerKey].deviceKeyList[index];//device to be removed taken in variable
        managerStruct[_managerKey].deviceKeyList[index] = managerStruct[_managerKey].deviceKeyList[deviceCount-1];//last device replaced
        delete(managerStruct[_managerKey].deviceKeyList[deviceCount-1]);
        managerStruct[_managerKey].deviceKeyList.length--;
        delete(managerStruct[_managerKey].deviceStruct[_deviceKey]);
    }

    function RemoveManager(bytes32 _managerKey)public payable returns(bytes32 managerToBeRemoved){
        uint managerCount = managerKeyList.length;
        uint index;
        for(uint i = 0; i < managerCount; i++){
           if(_managerKey == managerKeyList[i])
                index = i;
        }
        managerToBeRemoved = managerKeyList[index];//manager to be removed taken in variable
        managerKeyList[index] = managerKeyList[managerCount-1];//last device replaced
        delete(managerKeyList[managerCount-1]);
        managerKeyList.length--;
        delete(managerStruct[_managerKey]);
    }
}