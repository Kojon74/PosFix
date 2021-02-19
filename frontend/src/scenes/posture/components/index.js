import React from "react";
import { StyleSheet, Text, View } from "react-native";
import { AppProvider } from "../context";
import PostureScreen from "./PostureScreen";

const Screen = () => {
  return (
    <AppProvider>
      <PostureScreen />
    </AppProvider>
  );
};

export default Screen;

const styles = StyleSheet.create({});
