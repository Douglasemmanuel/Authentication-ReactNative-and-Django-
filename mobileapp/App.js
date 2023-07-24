import { NavigationContainer } from "@react-navigation/native";
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import UserLoginScreen from "./Screen/auth/UserLoginScreen";
import ShopTab from "./Screen/shop/ShopTab";
import RegistrationScreen from "./Screen/auth/RegistrationScreen";
import SendPasswordResetEmailScreen from "./Screen/auth/SendPasswordResetScrenEmailScreen";
import UserPanelTab from "./Screen/UserPanelTab";

import { Provider } from 'react-redux';
import { store } from './Screen/store';


const Stack = createNativeStackNavigator();

function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator screenOptions={{ headerStyle: { backgroundColor: 'purple' }, headerTintColor: 'white' }}>
        <Stack.Screen name="ShopTab" component={ShopTab} options={{ headerShown: false }} />
        <Stack.Screen name="UserLogin" component={UserLoginScreen} options={{ title: 'User Login' }} />
        <Stack.Screen name="Registration" component={RegistrationScreen} options={{ title: 'Registration', headerBackVisible: false }} />
        <Stack.Screen name="SendPasswordResetEmail" component={SendPasswordResetEmailScreen} options={{ title: 'Forgot Password' }} />
        <Stack.Screen name="UserPanelTab" component={UserPanelTab} options={{ headerShown: false }} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}

export default () {
return(
<Provider store={store}>
<App/>
</Provider>
 
)
}
