import React from "react";
import { StyleSheet, Text, View } from "react-native";
import { createMaterialTopTabNavigator } from "@react-navigation/material-top-tabs";

import HomeScreen from "./screens/HomeScreen";
import DailyScreen from "./screens/DailyScreen";
import DataScreen from "./screens/DataScreen";
import ProfileScreen from "./screens/ProfileScreen";

const Tab = createMaterialTopTabNavigator();

const colors = { primary: "#05386B", secondary: "#5CDB95" };

const TabBar = () => {
  return (
    <Tab.Navigator
      initialRouteName="Home"
      tabBarOptions={{
        activeTintColor: colors.primary,
        pressOpacity: 0.5,
        style: {
          backgroundColor: colors.secondary,
          shadowOpacity: 0,
          elevation: 0, // for Android
          shadowOffset: {
            width: 0,
            height: 0, // for iOS
          },
        },
        renderIndicator: () => null,
      }}
    >
      <Tab.Screen name="Home" component={HomeScreen} />
      <Tab.Screen name="Daily" component={DailyScreen} />
      <Tab.Screen name="Data" component={DataScreen} />
      <Tab.Screen name="Profile" component={ProfileScreen} />
    </Tab.Navigator>
  );
};

export default TabBar;

const styles = StyleSheet.create({});
