import React from "react";
import { StyleSheet, Text, View } from "react-native";
import { createMaterialTopTabNavigator } from "@react-navigation/material-top-tabs";

import { PostureScreen } from "../scenes/posture";
import { DailyScreen } from "../scenes/daily";
import { DataScreen } from "../scenes/data";
import { ProfileScreen } from "../scenes/profile";
import { Colors } from "../styles";

const Tab = createMaterialTopTabNavigator();

const TabBar = () => {
  return (
    <Tab.Navigator
      initialRouteName="Home"
      tabBarOptions={{
        activeTintColor: Colors.PRIMARY,
        pressOpacity: 0.5,
        style: {
          backgroundColor: Colors.SECONDARY,
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
      <Tab.Screen name="Posture" component={PostureScreen} />
      <Tab.Screen name="Daily" component={DailyScreen} />
      <Tab.Screen name="Data" component={DataScreen} />
      <Tab.Screen name="Profile" component={ProfileScreen} />
    </Tab.Navigator>
  );
};

export default TabBar;

const styles = StyleSheet.create({});
