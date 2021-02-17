import React from "react";
import { StyleSheet, Text, View } from "react-native";
import { createMaterialTopTabNavigator } from "@react-navigation/material-top-tabs";

import { PostureScreen } from "_scenes/posture";
import { DailyScreen } from "_scenes/daily";
import { DataScreen } from "_scenes/data";
import { ProfileScreen } from "_scenes/profile";
import { Colors } from "_styles";

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
      <Tab.Screen name="Home" component={PostureScreen} />
      <Tab.Screen name="Daily" component={DailyScreen} />
      <Tab.Screen name="Data" component={DataScreen} />
      <Tab.Screen name="Profile" component={ProfileScreen} />
    </Tab.Navigator>
  );
};

export default TabBar;

const styles = StyleSheet.create({});
