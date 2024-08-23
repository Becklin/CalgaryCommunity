/* eslint-disable react/prop-types */
import React from "react";
import { Button, InputNumber, Form } from "antd";
import "./style.css";

function WeightsForm(props) {
  const {
    onFinish,
    onFinishFailed,
    values,
    onCrimesChange,
    onServicesChange,
    onIncomeChange,
  } = props;
  return (
    <Form
      name="basic"
      style={{
        background: "white",
        padding: "10px",
      }}
      initialValues={{
        remember: true,
      }}
      onFinish={onFinish}
      onFinishFailed={onFinishFailed}
      autoComplete="off"
      layout="vertical"
    >
      <div
        style={{
          display: "flex",
          justifyContent: "space-around",
        }}
      >
        <Form.Item label="CRIMES">
          <InputNumber
            className="inputNumber"
            size="large"
            min={0}
            max={10}
            defaultValue={values.crimes}
            onChange={onCrimesChange}
          />
        </Form.Item>
        <Form.Item label="SERVICES">
          <InputNumber
            className="inputNumber"
            size="large"
            min={0}
            max={10}
            defaultValue={values.services}
            onChange={onServicesChange}
          />
        </Form.Item>
        <Form.Item label="INCOME">
          <InputNumber
            className="inputNumber"
            size="large"
            min={0}
            max={10}
            defaultValue={values.income}
            onChange={onIncomeChange}
          />
        </Form.Item>
      </div>
      <Form.Item>
        <Button
          className="submit-wrapper"
          type="primary"
          htmlType="submit"
          size="large"
        >
          CHECK
        </Button>
      </Form.Item>
    </Form>
  );
}

export default WeightsForm;
