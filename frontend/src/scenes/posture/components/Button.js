import React from "react";
import { StyleSheet, Text, TouchableOpacity } from "react-native";
import { Buttons } from "../../../styles";

const Button = ({ text, primary, handlePress, style }) => {
  return (
    <TouchableOpacity
      onPress={handlePress}
      style={[primary ? Buttons.BG_PRIMARY : Buttons.BG_SECONDARY, style]}
    >
      <Text style={primary ? Buttons.TXT_PRIMARY : Buttons.TXT_SECONDARY}>
        {text}
      </Text>
    </TouchableOpacity>
  );
};

export default Button;

const styles = StyleSheet.create({});
