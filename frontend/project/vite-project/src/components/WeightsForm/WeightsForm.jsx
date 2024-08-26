/* eslint-disable react/prop-types */
import React from "react";
import { Button, InputNumber, Form, Tooltip } from "antd";
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
        fontFamily: "Courier New', Courier, monospace",
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
      <Form.Item
        style={{
          textAlign: "right",
        }}
      >
        <Tooltip title="Total weights must be equal to 10">
          <span className="form-question">?</span>
        </Tooltip>
        <Button
          disabled={values.crimes + values.services + values.income !== 10}
          className="submit-wrapper"
          type="primary"
          htmlType="submit"
          size="small"
        >
          CHECK
        </Button>
      </Form.Item>
    </Form>
  );
}

export default WeightsForm;
