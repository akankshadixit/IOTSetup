pragma solidity ^0.5.13;
contract Greeter{
      string public greeting;
      event ChangeGreeting(string newGreeting);
      constructor()public{
          greeting = 'Hello Akanksha';
      }
      function setGreeting(string memory _greeting)public{
          greeting = _greeting;
          emit ChangeGreeting(_greeting);
      }
      function greet()public view returns(string memory){
          return greeting;
      }
}